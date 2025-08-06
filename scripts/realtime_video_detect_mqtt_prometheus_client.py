import cv2
import base64
import time
import argparse
import paho.mqtt.client as mqtt
from ultralytics import YOLO
from yt_dlp import YoutubeDL
from prometheus_client import start_http_server, Gauge

# Supervision (for better annotation and ByteTrack)
import supervision as sv

# ---------- Argument parser ------------------
parser = argparse.ArgumentParser(description="Object detection MQTT with Tracking")
parser.add_argument("--ip", type=str, required=True, help="IP address of Tailscale machine")
parser.add_argument('--port', type=int, default=1883, help='Port of MQTT broker (default: 1883)')
parser.add_argument('--metrics_port', type=int, default=8000, help='Prometheus metrics port')
args = parser.parse_args()

# MQTT setup
MQTT_BROKER = args.ip
MQTT_PORT = args.port
MQTT_TOPIC = "video/stream"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# 🔍 Prometheus metrics
start_http_server(args.metrics_port)  # Prometheus scrapes here
fps_gauge = Gauge('yolo_fps', 'Frames per second')
inference_time_gauge = Gauge('yolo_inference_time_ms', 'Inference time per frame in ms')
detection_count_gauge = Gauge('yolo_detection_count', 'Number of detections per frame')

# ---------- Supervision + ByteTrack -----------
tracker = sv.ByteTrack()  # Multi-object tracking
box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=2,
    text_scale=0.6
)


def run_realtime_detection(video_url):
    model = YOLO("models/yolo11n.pt")
    cap = cv2.VideoCapture(video_url)

    if not cap.isOpened():
        print("Error: Video source not accessible")
        return

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        start_infer = time.time()
        results = model(frame, verbose=False)
        end_infer = time.time()

        # Update metrics
        inference_ms = (end_infer - start_infer) * 1000
        inference_time_gauge.set(inference_ms)

        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        fps_gauge.set(fps)
        prev_time = curr_time

        detection_count = len(results[0].boxes) if results else 0
        detection_count_gauge.set(detection_count)

        # Convert YOLO results to Supervision Detections
        detections = sv.Detections.from_ultralytics(results[0])

        # Update tracker with current frame detections
        tracked_detections = tracker.update_with_detections(detections)

        # Annotate frame with bounding boxes + IDs
        labels = [
            f"ID {tracker_id} {model.names[class_id]}"
            for _, _, class_id, _, tracker_id in tracked_detections
        ]
        annotated_frame = box_annotator.annotate(scene=frame.copy(), detections=tracked_detections, labels=labels)

        # Encode and publish frame over MQTT
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        client.publish(MQTT_TOPIC, jpg_as_text)

        # Display locally for debugging (optional)
        cv2.imshow("YOLO Real-Time Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.03)  # ~30 FPS cap

    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()


if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=u4UZ4UvZXrg"

    # Extract best video URL
    ydl_opts = {'format': 'best'}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        video_url = info['url']

    print("Direct stream URL:", video_url)
    run_realtime_detection(video_url)

import cv2
import base64
import paho.mqtt.client as mqtt
from ultralytics import YOLO
import time
import argparse



#----------Argument parser------------------
parser=argparse.ArgumentParser(description="Object detection MQTT")
parser.add_argument("--ip",type=str, required=True, help="IP address of Tailscale machine")
parser.add_argument('--port', type=int, default=1883, help='Port of MQTT broker (default: 1883)')
args = parser.parse_args()
# MQTT setup
MQTT_BROKER = args.ip  # Replace with your broker's IP or domain
MQTT_PORT = args.port
MQTT_TOPIC = "video/stream"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def run_realtime_detection():
    model = YOLO("models/yolo11n.pt")
    cap = cv2.VideoCapture(0)  # Use webcam

    if not cap.isOpened():
        print("Error: Webcam not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated_frame = results[0].plot()

        # Display locally
        #cv2.imshow("YOLO Real-Time Detection", annotated_frame)

        # Encode and publish frame over MQTT
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        client.publish(MQTT_TOPIC, jpg_as_text)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.03)  # Throttle to ~30 FPS

    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()

if __name__ == "__main__":
    run_realtime_detection()

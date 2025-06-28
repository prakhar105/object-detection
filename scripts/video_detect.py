import cv2
from ultralytics import YOLO
import os

def run_video_detection(video_path, output_path):
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(video_path)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()
    print(f"Detection complete. Saved to {output_path}")

if __name__ == "__main__":
    input_video = "videos/input.mp4"
    output_video = "outputs/annotated_output.mp4"
    os.makedirs("outputs", exist_ok=True)
    run_video_detection(input_video, output_video)
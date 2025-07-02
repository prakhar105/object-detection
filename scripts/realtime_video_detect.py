import cv2
from ultralytics import YOLO

def run_realtime_detection():
    model = YOLO("models/yolo11n.pt")  # Your YOLO model path
    cap = cv2.VideoCapture(0)  # 0 = default webcam

    if not cap.isOpened():
        print("Error: Webcam not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated_frame = results[0].plot()

        cv2.imshow("YOLO Real-Time Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_realtime_detection()

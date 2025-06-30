import os
from ultralytics import YOLO
import cv2

def test_model_load():
    model = YOLO("models/yolo11n.pt")
    assert model is not None

def test_video_detection_runs():
    model = YOLO("models/yolo11n.pt")
    frame = cv2.imread("videos/Screenshot 2025-06-30 204816.png")  # add a small test image
    assert frame is not None, "Test image missing"
    results = model(frame)
    assert len(results) > 0
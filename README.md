# 🎥 YOLOv8 Video Object Detection

This project demonstrates object detection using [Ultralytics YOLOv8](https://docs.ultralytics.com/) on video files. It also includes a GitHub Actions CI pipeline that automatically tests the object detection script whenever you push changes to the repository.

---

## 🚀 Features

- Detect objects frame-by-frame in video files using YOLOv8
- Save the output as an annotated video
- CI pipeline using GitHub Actions for automatic testing
- Lightweight and easy to extend with custom models

---

## 🗂️ Project Structure

```
yolo-video-detection/
│
├── videos/
│   └── input.mp4                # Sample input video
│
├── outputs/
│   └── annotated_output.mp4     # Output video after detection
│
├── scripts/
│   └── video_detect.py          # YOLOv8 video detection script
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .github/
    └── workflows/
        └── ci.yml               # GitHub Actions CI workflow
```

---

## 🧠 How It Works

- Loads a pretrained YOLOv8n model.
- Reads video frames from `videos/input.mp4`.
- Applies detection on each frame.
- Annotates and saves the video to `outputs/annotated_output.mp4`.

---

## 🧪 Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/yolo-video-detection.git
cd yolo-video-detection
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Input Video

Place your input video inside the `videos/` folder and name it `input.mp4`.

### 4. Run Detection

```bash
python scripts/video_detect.py
```

---

## ✅ CI/CD with GitHub Actions

Every push or pull request to the `main` branch triggers:

- Code checkout
- Python environment setup
- Dependency installation
- Dry run of the detection script

📄 See `.github/workflows/ci.yml` for details.

---

## 🧩 Customize

Want to use your own model?

Just replace `"yolov8n.pt"` with the path to your trained model:

```python
model = YOLO("path/to/your/best.pt")
```

---

## 📦 Requirements

- Python 3.8+
- `ultralytics`
- `opencv-python`

---

## 📸 Output Preview

Annotated videos will be saved to the `outputs/` directory.

---

## 🛠️ TODOs

- [ ] Add support for real-time webcam detection
- [ ] Integrate with a web UI (e.g., Streamlit or Flask)
- [ ] Auto-download sample videos if none exist

---

## 🤝 License

MIT License – feel free to use, modify, and share.

---

## 💡 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)

# 🎥 YOLO Video Object Detection

This project demonstrates object detection using [Ultralytics](https://docs.ultralytics.com/) on video files. It also includes a robust CI/CD pipeline using GitHub Actions, test-driven development (TDD), and optional data versioning using DVC.

---

## 🚀 Features

- Detect objects frame-by-frame in video files using YOLOv8
- Save the output as an annotated video
- Unit tests using `pytest` (TDD-friendly)
- CI pipeline using GitHub Actions for automatic testing
- DVC support for tracking videos and models
- Lightweight and easy to extend with custom models

---

## 🗂️ Project Structure

```
object-detection-ci-cd-tdd-dvc/
│
├── videos/
│   └── input.mp4                # Sample input video (DVC tracked)
│
├── outputs/
│   └── annotated_output.mp4     # Output video after detection
│
├── scripts/
│   └── video_detect.py          # YOLOv8 video detection script
│
├── tests/
│   └── test_detect.py           # Unit tests for model loading and detection
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── dvc.yaml                     # Optional DVC pipeline
├── .dvc/                        # DVC metadata
└── .github/
    └── workflows/
        └── ci.yml               # GitHub Actions CI workflow
```

---

## 🧠 How It Works

- Loads a pretrained YOLOv11n model.
- Reads video frames from `videos/input.mp4`.
- Applies detection on each frame.
- Annotates and saves the video to `outputs/annotated_output.mp4`.

---

## 🧪 Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/object-detection-ci-cd-tdd-dvc.git
cd object-detection-ci-cd-tdd-dvc
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

## 🧪 Run Tests

Make sure the `tests/` folder has test files named like `test_*.py`. Then run:

```bash
pytest tests/
```

Tests include:
- Model loading
- Single frame inference sanity check

---

## ✅ CI/CD with GitHub Actions

Every push or pull request to the `main` branch triggers:

- Code checkout
- Python environment setup
- Dependency installation
- Unit tests execution with `pytest`

📄 See `.github/workflows/ci.yml` for details.

---

## 📦 Data & Model Versioning with DVC

DVC can be used to version control large files like videos and models.

```bash
dvc add videos/input.mp4
dvc add yolov8n.pt
dvc push
```
![DVC Flow Diagram](https://github.com/prakhar105/object-detection-ci-cd-tdd-dvc/blob/main/data/DVC.png)

Add a remote storage (Google Drive, S3, etc.) to manage large files.

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
- `pytest` (for testing)
- `dvc` (optional, for versioning)

---

## 📸 Output Preview

Annotated videos will be saved to the `outputs/` directory.

---

## 🛠️ TODOs

- [x] Add unit tests (TDD)
- [x] Setup GitHub Actions CI
- [x] Integrate DVC
- [ ] Add support for real-time webcam detection
- [ ] Integrate with a web UI (e.g., Streamlit or Flask)
- [ ] Auto-download sample videos if none exist

---

## 🤝 License

MIT License – feel free to use, modify, and share.

---

## 💡 Acknowledgments

- [Ultralytics YOLOv11](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [DVC](https://dvc.org/)
- [pytest](https://docs.pytest.org/)

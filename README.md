# 🎥 YOLO Video Object Detection

This project demonstrates object detection using [Ultralytics](https://docs.ultralytics.com/) on video files. It also includes a robust CI/CD pipeline using GitHub Actions, test-driven development (TDD), and optional data versioning using DVC.

---
## 🔄 Architecture
```
+------------------------+       +------------------------+
|  Jetson Edge Device    |       |   Root Control Node    |
|  (Ansible Managed)     |       |                        |
|                        |       |                        |
|  - YOLOv8 Inference    |       |  - Receives MQTT data  |
|  - MQTT Publisher      +------->  - Visualizes results  |
|  - Auto-start via svc  |       |                        |
+------------------------+       +------------------------+
        ^                                ^
        |                                |
     [Tailscale VPN: Secure Mesh Networking]
```
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

# 🚀 Step-by-Step: SSH Key Setup for Jetson with Ansible (WSL-Compatible)

This guide explains how to set up SSH keys to connect from your **Ansible control machine (WSL)** to a **Jetson device** over SSH, and how to enable remote SSH access *into* WSL as well.  

---

## 🔐 Part A: Setup SSH Access from WSL (Control Node) to Jetson

### 1. Generate SSH Key (on WSL)

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

> 💡 Save it in the default path `/home/your_user/.ssh/id_rsa` (not inside `/mnt/c/...` to avoid permission errors).

### 2. Set Proper Permissions

```bash
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

### 3. Copy Public Key to Jetson

Replace the IP and user with your Jetson device's settings:

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub host_device_name@<host_device_tailscale device IP>
```

Test SSH login (should not ask for password):

```bash
ssh -i ~/.ssh/id_rsa host_device_name@<tailscale device IP>
```

---

## 📦 Part B: Configure Ansible Inventory

Example `inventory/hosts.ini`:

```ini
[jetson]
host_device_name ansible_host=<tailscale device IP> ansible_user=host_device_name ansible_ssh_private_key_file=/home/your_user/.ssh/id_rsa
```
![Tailscale](https://github.com/prakhar105/object-detection-ci-cd-tdd-dvc/blob/main/data/tailscale.png)
![Ansible](https://github.com/prakhar105/object-detection-ci-cd-tdd-dvc/blob/main/data/ansible.png)

---

## ▶️ Part C: Run Ansible Playbook

Use this command to run your Ansible script:

```bash
ansible-playbook -i inventory/hosts.ini playbooks/install.yml --ask-become-pass
```
This Ansible script will configure the device, download updated git repository, create uv venv, install requirements.txt, will execute the object detection and publish detection data Tailscale host device IP using MQTT protocol.

---

## ▶️ Part D: Execute MQTT Subscriber on Root Device

```
uv run .\scripts\mqtt_subscriber.py --ip <host_device_tailscale_IP>
```
---
## 🛠 Notes

- For cross-network access, use [Tailscale](https://tailscale.com).
- Ensure Jetson's SSH server is running: `sudo systemctl status ssh`
- You can set up hostnames using `/etc/hosts` or `.ssh/config`.

---

## 📁 Directory Structure Example

```
jetson_setup/
├── .ssh/
│   └── id_rsa, id_rsa.pub
├── inventory/
│   └── hosts.ini
└── playbooks/
    └── install.yml
```



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

import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import argparse
import tkinter as tk
from PIL import Image, ImageTk
import threading

parser = argparse.ArgumentParser(description="MQTT Video Stream GUI")
parser.add_argument("--ip", type=str, required=True, help="IP address of Tailscale machine")
parser.add_argument("--port", type=int, default=1883, help="Port of MQTT broker (default: 1883)")
args = parser.parse_args()

# ---------------- Tkinter GUI Setup ----------------
root = tk.Tk()
root.title("MQTT Video Stream")
root.geometry("1280x720")  # Initial window size

video_label = tk.Label(root, bg="black")
video_label.pack(fill=tk.BOTH, expand=True)

# Global frame storage for smooth updates
latest_frame = None
lock = threading.Lock()

# ---------------- MQTT Callbacks -------------------
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("video/stream")

def on_message(client, userdata, msg):
    global latest_frame
    jpg_original = base64.b64decode(msg.payload)
    np_arr = np.frombuffer(jpg_original, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Store frame thread-safely
    with lock:
        latest_frame = frame_rgb

# ---------------- MQTT Client Setup ----------------
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(args.ip, args.port, 60)
client.loop_start()

# ---------------- GUI Update Loop ------------------
def update_frame():
    global latest_frame
    frame_copy = None

    with lock:
        if latest_frame is not None:
            frame_copy = latest_frame.copy()

    if frame_copy is not None:
        # Convert to Image for Tkinter
        img = Image.fromarray(frame_copy)
        img = img.resize((root.winfo_width(), root.winfo_height()))
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # Schedule next update (about 30 FPS)
    root.after(33, update_frame)

# ---------------- Window Close Handling ----------------
def on_close():
    print("Closing GUI...")
    client.disconnect()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# Start GUI update loop
update_frame()
root.mainloop()

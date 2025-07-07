import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import argparse

parser=argparse.ArgumentParser(description="Object detection MQTT")
parser.add_argument("--ip",type=str, required=True, help="IP address of Tailscale machine")
parser.add_argument('--port', type=int, default=1883, help='Port of MQTT broker (default: 1883)')
args = parser.parse_args()


def on_connect(client, userdata, flags, rc):
    client.subscribe("video/stream")

def on_message(client, userdata, msg):
    jpg_original = base64.b64decode(msg.payload)
    np_arr = np.frombuffer(jpg_original, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    cv2.imshow("MQTT Video Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(args.ip, args.port, 60)
client.loop_forever()

import base64
import json
import requests

IMAGE_PATH = "/home/chase/desk_items_conversion/raw_images/jpeg_updated/IMG_9872.jpeg"
SERVER_URL = "http://127.0.0.1:9001/infer/object_detection"
MODEL_ID = "desk_items-8-rfdetr-small-t1"

with open(IMAGE_PATH, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "id": "desk-items-first-local-test",
    "model_id": MODEL_ID,
    "image": {
        "type": "base64",
        "value": image_base64,
    },
    "confidence": "best",
    "visualize_predictions": True,
    "visualization_labels": True,
}

response = requests.post(SERVER_URL, json=payload)

print("HTTP status:", response.status_code)

response.raise_for_status()

result = response.json()

print(json.dumps(result, indent=2))

import os
from pathlib import Path

from inference_sdk import InferenceHTTPClient, InferenceConfiguration
from PIL import Image, ImageDraw, ImageFont


IMAGE_PATH = Path(
    "/home/chase/desk_items_conversion/raw_images/jpeg_updated/IMG_9872.jpeg"
)

OUTPUT_PATH = Path(
    "/home/chase/desk_items_deployment/results/IMG_9872_detected.jpg"
)

WORKSPACE = "chase-gurcan-s-workspace"
WORKFLOW_ID = "deskitems-vdeskitems-8-rfdetr-small-t1-logic"


# Create output directory
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# Connect to local Roboflow inference server
client = InferenceHTTPClient(
    api_url="http://localhost:9001",
    api_key=os.environ["ROBOFLOW_API_KEY"],
).configure(
    InferenceConfiguration(
        api_key_transport="header"
    )
)


# Run the trained model locally
result = client.run_workflow(
    workspace_name=WORKSPACE,
    workflow_id=WORKFLOW_ID,
    images={
        "image": str(IMAGE_PATH)
    },
    use_cache=True,
)


# Get predictions
predictions = result[0]["predictions"]["predictions"]

print(f"\nImage: {IMAGE_PATH.name}")
print(f"Detections: {len(predictions)}\n")


# Load image
image = Image.open(IMAGE_PATH).convert("RGB")
draw = ImageDraw.Draw(image)


# Draw each detection
for prediction in predictions:
    x = prediction["x"]
    y = prediction["y"]
    width = prediction["width"]
    height = prediction["height"]

    confidence = prediction["confidence"]
    class_name = prediction["class"]

    left = x - width / 2
    top = y - height / 2
    right = x + width / 2
    bottom = y + height / 2

    # Bounding box
    draw.rectangle(
        [left, top, right, bottom],
        outline="red",
        width=8,
    )

    # Label
    label = f"{class_name} {confidence:.1%}"

    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            48,
        )
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((left, top), label, font=font)

    # Label background
    draw.rectangle(
        bbox,
        fill="red",
    )

    # Label text
    draw.text(
        (left, top),
        label,
        fill="white",
        font=font,
    )

    print(
        f"- {class_name}: "
        f"{confidence:.1%} "
        f"box=({left:.0f}, {top:.0f}, {right:.0f}, {bottom:.0f})"
    )


# Save visualization
image.save(OUTPUT_PATH, quality=95)

print(f"\nSaved visualization to:")
print(OUTPUT_PATH)

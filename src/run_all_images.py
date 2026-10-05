import os
from pathlib import Path

from inference_sdk import InferenceHTTPClient, InferenceConfiguration
from PIL import Image, ImageDraw, ImageFont


# --------------------------------------------------
# Configuration
# --------------------------------------------------

VERSION = "v8_rfdetr_small"

INPUT_DIR = Path(
    "/home/chase/desk_items_conversion/raw_images/jpeg_updated"
)

OUTPUT_DIR = Path(
    f"/home/chase/desk_items_deployment/results/{VERSION}"
)

WORKSPACE = "chase-gurcan-s-workspace"

WORKFLOW_ID = (
    "deskitems-vdeskitems-8-rfdetr-small-t1-logic"
)

MODEL_ID = "desk_items-8-rfdetr-small-t1"


# Create version-specific output directory
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# Connect to local Roboflow inference server
# --------------------------------------------------

client = InferenceHTTPClient(
    api_url="http://localhost:9001",
    api_key=os.environ["ROBOFLOW_API_KEY"],
).configure(
    InferenceConfiguration(
        api_key_transport="header"
    )
)


# --------------------------------------------------
# Font for visualization labels
# --------------------------------------------------

try:
    FONT = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        48,
    )
except OSError:
    FONT = ImageFont.load_default()


# --------------------------------------------------
# Find input images
# --------------------------------------------------

images = sorted(
    list(INPUT_DIR.glob("*.jpg"))
    + list(INPUT_DIR.glob("*.jpeg"))
    + list(INPUT_DIR.glob("*.JPG"))
    + list(INPUT_DIR.glob("*.JPEG"))
)

print("=" * 60)
print("DESK_ITEMS BATCH INFERENCE")
print("=" * 60)
print(f"Version:             {VERSION}")
print(f"Model:               {MODEL_ID}")
print(f"Workflow:            {WORKFLOW_ID}")
print(f"Input directory:     {INPUT_DIR}")
print(f"Output directory:    {OUTPUT_DIR}")
print(f"Images found:        {len(images)}")
print("=" * 60)
print()


if not images:
    raise RuntimeError(
        f"No images found in {INPUT_DIR}"
    )


# --------------------------------------------------
# Process images
# --------------------------------------------------

total_detections = 0
successful = 0
failed = 0


for index, image_path in enumerate(
    images,
    start=1,
):

    print(
        f"[{index}/{len(images)}] "
        f"{image_path.name}",
        end=" ... ",
        flush=True,
    )

    try:

        # ------------------------------------------
        # Run local inference
        # ------------------------------------------

        result = client.run_workflow(
            workspace_name=WORKSPACE,
            workflow_id=WORKFLOW_ID,
            images={
                "image": str(image_path)
            },
            use_cache=False,
        )

        predictions = (
            result[0]
            ["predictions"]
            ["predictions"]
        )

        total_detections += len(predictions)


        # ------------------------------------------
        # Load original image
        # ------------------------------------------

        image = Image.open(
            image_path
        ).convert("RGB")

        draw = ImageDraw.Draw(image)


        # ------------------------------------------
        # Draw predictions
        # ------------------------------------------

        for prediction in predictions:

            x = prediction["x"]
            y = prediction["y"]

            width = prediction["width"]
            height = prediction["height"]

            confidence = prediction["confidence"]
            class_name = prediction["class"]


            # Convert center coordinates to
            # bounding-box corners

            left = x - width / 2
            top = y - height / 2
            right = x + width / 2
            bottom = y + height / 2


            # Bounding box

            draw.rectangle(
                [
                    left,
                    top,
                    right,
                    bottom,
                ],
                outline="red",
                width=8,
            )


            # Label

            label = (
                f"{class_name} "
                f"{confidence:.1%}"
            )

            text_bbox = draw.textbbox(
                (left, top),
                label,
                font=FONT,
            )


            # Label background

            draw.rectangle(
                text_bbox,
                fill="red",
            )


            # Label text

            draw.text(
                (left, top),
                label,
                fill="white",
                font=FONT,
            )


        # ------------------------------------------
        # Save visualization
        # ------------------------------------------

        output_path = (
            OUTPUT_DIR /
            image_path.name
        )

        image.save(
            output_path,
            quality=95,
        )


        successful += 1

        print(
            f"{len(predictions)} detections"
        )


    except Exception as e:

        failed += 1

        print(
            f"FAILED: "
            f"{type(e).__name__}: {e}"
        )


# --------------------------------------------------
# Final summary
# --------------------------------------------------

print()
print("=" * 60)
print("BATCH INFERENCE COMPLETE")
print("=" * 60)

print(
    f"Version:             {VERSION}"
)

print(
    f"Model:               {MODEL_ID}"
)

print(
    f"Images found:        {len(images)}"
)

print(
    f"Successful:          {successful}"
)

print(
    f"Failed:              {failed}"
)

print(
    f"Total detections:    {total_detections}"
)

if successful > 0:
    average_detections = (
        total_detections / successful
    )

    print(
        f"Average detections:  "
        f"{average_detections:.2f}"
        f" per image"
    )

print()
print(
    "Visualizations saved to:"
)

print(OUTPUT_DIR)

print("=" * 60)

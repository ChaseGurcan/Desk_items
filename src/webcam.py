import os
import cv2
import threading
import time

from inference_sdk import InferenceHTTPClient, InferenceConfiguration


# ============================================================
# Configuration
# ============================================================

WORKSPACE = "chase-gurcan-s-workspace"
WORKFLOW_ID = "deskitems-vdeskitems-8-rfdetr-small-t1-logic"

API_URL = "http://localhost:9001"

# Insta360 Link 2
CAMERA_INDEX = 2

# V8 optimal confidence threshold
CONFIDENCE_THRESHOLD = 0.48


# ============================================================
# Shared state between threads
# ============================================================

latest_frame = None
latest_result = []

frame_lock = threading.Lock()
result_lock = threading.Lock()
performance_lock = threading.Lock()

running = True

# Performance measurements
display_fps = 0.0
inference_ms = 0.0

display_count = 0
fps_start_time = time.time()


# ============================================================
# Roboflow client
# ============================================================

api_key = os.environ.get("ROBOFLOW_API_KEY")

if not api_key:
    raise RuntimeError(
        "ROBOFLOW_API_KEY is not set.\n"
        "Run: export ROBOFLOW_API_KEY='YOUR_KEY'"
    )

client = InferenceHTTPClient(
    api_url=API_URL,
    api_key=api_key,
).configure(
    InferenceConfiguration(
        api_key_transport="header"
    )
)


# ============================================================
# Camera thread
# ============================================================

def camera_loop():

    global latest_frame
    global running

    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print(
            f"ERROR: Could not open camera index "
            f"{CAMERA_INDEX}."
        )
        running = False
        return

    print(f"Camera opened: /dev/video{CAMERA_INDEX}")

    while running:

        ret, frame = cap.read()

        if not ret:
            print("WARNING: Failed to read camera frame.")
            continue

        with frame_lock:
            latest_frame = frame.copy()

    cap.release()


# ============================================================
# Inference thread
# ============================================================

def inference_loop():

    global latest_result
    global running
    global inference_ms

    while running:

        # Get newest available frame
        with frame_lock:

            if latest_frame is None:
                time.sleep(0.01)
                continue

            frame = latest_frame.copy()

        try:

            # Start inference timer
            inference_start = time.perf_counter()

            result = client.run_workflow(
                workspace_name=WORKSPACE,
                workflow_id=WORKFLOW_ID,
                images={
                    "image": frame
                },
                use_cache=False,
            )

            # Stop inference timer
            inference_end = time.perf_counter()

            inference_time = (
                inference_end - inference_start
            ) * 1000

            with performance_lock:
                inference_ms = inference_time

            # Extract predictions
            try:
                predictions = (
                    result[0]
                    ["predictions"]
                    ["predictions"]
                )

            except (
                KeyError,
                IndexError,
                TypeError,
            ):
                predictions = []

            # Store newest predictions
            with result_lock:
                latest_result = predictions

        except Exception as e:

            print(f"Inference error: {e}")

            time.sleep(0.1)


# ============================================================
# Start application
# ============================================================

print("=" * 60)
print("DESK ITEMS - LIVE WEBCAM INFERENCE")
print("=" * 60)
print(f"Camera:              /dev/video{CAMERA_INDEX}")
print(f"Model:               desk_items-8-rfdetr-small-t1")
print(f"Workflow:            {WORKFLOW_ID}")
print(f"Confidence threshold: {CONFIDENCE_THRESHOLD}")
print()
print("Press Q to quit.")
print("Ctrl+C also stops the application.")
print("=" * 60)


camera_thread = threading.Thread(
    target=camera_loop,
    daemon=True,
)

inference_thread = threading.Thread(
    target=inference_loop,
    daemon=True,
)

camera_thread.start()
inference_thread.start()


# ============================================================
# Display loop
# ============================================================

try:

    while running:

        # ----------------------------------------------------
        # Get newest camera frame
        # ----------------------------------------------------

        with frame_lock:

            if latest_frame is None:
                time.sleep(0.01)
                continue

            display_frame = latest_frame.copy()

        # ----------------------------------------------------
        # Get newest predictions
        # ----------------------------------------------------

        with result_lock:
            predictions = list(latest_result)

        # ----------------------------------------------------
        # Calculate display FPS
        # ----------------------------------------------------

        display_count += 1

        elapsed = time.time() - fps_start_time

        if elapsed >= 1.0:

            display_fps = (
                display_count / elapsed
            )

            display_count = 0
            fps_start_time = time.time()

        # ----------------------------------------------------
        # Draw predictions
        # ----------------------------------------------------

        detection_count = 0

        for prediction in predictions:

            confidence = prediction.get(
                "confidence",
                0
            )

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            detection_count += 1

            class_name = prediction.get(
                "class",
                "unknown"
            )

            x = prediction["x"]
            y = prediction["y"]

            width = prediction["width"]
            height = prediction["height"]

            # Convert center coordinates
            # to bounding-box corners

            x1 = int(
                x - width / 2
            )

            y1 = int(
                y - height / 2
            )

            x2 = int(
                x + width / 2
            )

            y2 = int(
                y + height / 2
            )

            # ------------------------------------------------
            # Bounding box
            # ------------------------------------------------

            cv2.rectangle(
                display_frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2,
            )

            # ------------------------------------------------
            # Detection label
            # ------------------------------------------------

            label = (
                f"{class_name} "
                f"{confidence:.0%}"
            )

            cv2.putText(
                display_frame,
                label,
                (
                    x1,
                    max(y1 - 10, 20)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

        # ----------------------------------------------------
        # Performance information
        # ----------------------------------------------------

        with performance_lock:
            current_inference_ms = inference_ms

        cv2.putText(
            display_frame,
            f"FPS: {display_fps:.1f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            display_frame,
            f"Inference: {current_inference_ms:.1f} ms",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            display_frame,
            f"Detections: {detection_count}",
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        cv2.imshow(
            "Desk Items - V8 RF-DETR Small",
            display_frame,
        )

        # ----------------------------------------------------
        # Keyboard input
        # ----------------------------------------------------

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            running = False
            break


except KeyboardInterrupt:

    print()
    print("Stopping webcam...")


finally:

    # --------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------

    running = False

    cv2.destroyAllWindows()

    print("Webcam stopped.")

# Architecture Documentation

## High-level architecture

``` text
Insta360 Link 2
      ↓
/dev/video2
      ↓
Python webcam.py
      ↓
inference-sdk
      ↓
localhost:9001
      ↓
Roboflow Inference Server
      ↓
RF-DETR Small
      ↓
class / confidence / x / y / width / height
      ↓
OpenCV visualization
```

## Runtime architecture

The final webcam application separates three activities.

### 1. Camera thread

Continuously reads frames from the camera and updates `latest_frame`.

### 2. Inference thread

Copies the newest available frame, sends it to the local inference
server, measures inference duration, extracts predictions, and updates
`latest_result`.

### 3. Display loop

Copies the newest frame and predictions, filters predictions below the
48% confidence threshold, converts center-coordinate boxes to corner
coordinates, draws the results, and handles keyboard input.

## Thread synchronization

The application uses:

``` text
frame_lock
result_lock
performance_lock
```

`frame.copy()` protects the application from sharing the same mutable
image buffer across threads.

## Prediction geometry

Roboflow returns:

``` text
x = center x
y = center y
width
height
```

The application converts these into:

``` text
x1 = x - width / 2
y1 = y - height / 2
x2 = x + width / 2
y2 = y + height / 2
```

for OpenCV rectangle drawing.

## Why threading improved the demo

Synchronous design:

``` text
capture → wait for inference → draw → repeat
```

Threaded design:

``` text
Camera ───────→ newest frame
                   ↓
Inference ────→ newest result
                   ↓
Display ──────→ continuous visualization
```

The display no longer has to block while every inference call completes.

## What the local system proves

The project demonstrates the complete perception path:

1.  Camera image enters the application.
2.  Python sends the image to a local inference service.
3.  The selected RF-DETR Small model produces object predictions.
4.  Python receives class, confidence, and bounding-box geometry.
5.  OpenCV renders the detections.

## What it does not yet prove

The current laptop/MX250 setup does not establish production robot
performance.

A production system still needs measurement on the target robot
hardware, including total end-to-end latency and sustainable inference
throughput.

## Security

The Roboflow API key is provided through `ROBOFLOW_API_KEY` and must
never be committed to GitHub.

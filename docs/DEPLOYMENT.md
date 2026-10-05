# Deployment Documentation

## Goal

Run the final RF-DETR Small model locally instead of relying on a remote
inference API for every camera frame.

## Deployment project

``` text
~/desk_items_deployment/
├── .venv/
├── src/
├── test_images/
├── results/
└── README.md
```

## Environment

The deployment environment uses Python 3.13 in a `uv` virtual
environment.

``` bash
cd ~/desk_items_deployment
uv venv --python 3.13 .venv
source .venv/bin/activate
```

## Roboflow inference server

The selected path was Roboflow self-hosted inference.

The server listens locally at:

``` text
http://127.0.0.1:9001
```

Docker runs the inference server.

## GPU

The development machine uses:

-   NVIDIA GeForce MX250
-   4 GB VRAM
-   NVIDIA driver 580.178.04
-   CUDA-compatible PyTorch build
-   NVIDIA Container Toolkit
-   Docker GPU support

GPU support was verified through an NVIDIA CUDA Docker container.

## API client

The deployment uses:

``` bash
uv pip install inference-sdk
```

The Roboflow key is supplied through:

``` bash
export ROBOFLOW_API_KEY='YOUR_CURRENT_ROBOFLOW_API_KEY'
```

Never commit this value.

## Final workflow

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
desk_items-8-rfdetr-small-t1
      ↓
detections
      ↓
OpenCV display
```

## Batch validation

78 images were processed:

``` text
Images found: 78
Successful: 78
Failed: 0
Total detections: 237
Average detections/image: 3.04
```

Versioned output was written to:

``` text
~/desk_items_deployment/results/v8_rfdetr_small
```

## Webcam

Camera:

``` text
Insta360 Link 2
/dev/video2
```

The first synchronous webcam implementation was slow because each camera
frame waited for inference.

The final implementation separates camera capture, inference, and
display using Python threads. This made the visual demo substantially
smoother.

## Important performance distinction

The final local workflow call was approximately 477 ms in the tested
setup, equivalent to roughly 2.1 fresh workflow results per second.

The displayed OpenCV FPS is the display-loop rate, not model inference
FPS.

The 4.9 ms Roboflow/serverless metric should also not be described as
local end-to-end latency.

## Restart

``` bash
cd ~/desk_items_deployment
source .venv/bin/activate
export ROBOFLOW_API_KEY='YOUR_CURRENT_ROBOFLOW_API_KEY'

docker info
curl http://127.0.0.1:9001/

python3 webcam.py
```

## Future deployment step

Benchmark the complete perception pipeline on the actual target robot
hardware, including camera capture, preprocessing, inference,
postprocessing, and application overhead.

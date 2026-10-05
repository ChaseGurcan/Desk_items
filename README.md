# Desk_items

Computer vision object-detection project demonstrating how Roboflow can
be used to build and locally deploy a lightweight detector for a
commercial office-cleaning robot use case.

## Problem

A commercial cleaning company deploys robots to clean office
environments. The robot needs to recognize common office objects so its
perception system can understand its environment.

The project was intentionally scoped as a quick demonstration: build an
object detector for six common office objects, evaluate the major
engineering tradeoffs, and demonstrate the final model locally.

## Classes

-   Charger
-   Computer
-   Mouse
-   Mug
-   Notebook
-   Pen

## Development process

``` text
Customer use case
      ↓
Image collection
      ↓
HEIC → JPEG
      ↓
Roboflow annotation
      ↓
Dataset versions
      ↓
Model experiments
      ↓
Evaluation
      ↓
Model selection
      ↓
Local self-hosted inference
      ↓
Batch + live-camera validation
```

## Final model

-   Roboflow Version: **v8 ---
    `v6 - targeted data expansion w known model`**
-   Model: **RF-DETR Small**
-   Model ID: `desk_items-8-rfdetr-small-t1`
-   Input: Auto-Orient + 512×512
-   Augmentation: none
-   Dataset: 292 images
-   Split: 200 train / 48 validation / 44 test
-   20 office-environment images were explicitly held out in Test.

## Final evaluation

  Metric                                 Result
  ------------------------------------ --------
  mAP@50                                  93.0%
  mAP@75                                  78.2%
  mAP@50:95                               76.9%
  Precision                               91.6%
  Recall                                  87.6%
  F1                                      89.5%
  Optimal confidence                        48%
  Median Roboflow/serverless latency     4.9 ms

The 4.9 ms number is a Roboflow/serverless model-latency measurement,
not end-to-end local webcam latency.

## Local architecture

``` text
Insta360 Link 2
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
class + confidence + bounding box
      ↓
OpenCV display
```

## Repository structure

``` text
desk_items/
├── README.md
├── .gitignore
├── requirements.txt
├── LICENSE
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── DATASET.md
│   ├── EXPERIMENT_LOG.md
│   ├── DEPLOYMENT.md
│   └── ARCHITECTURE.md
├── src/
├── scripts/
├── configs/
├── results/
└── presentations/
```

Raw images, API keys, virtual environments, model caches, and large
generated output directories should remain outside Git.

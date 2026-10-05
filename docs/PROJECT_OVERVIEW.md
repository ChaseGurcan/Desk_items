# Project Overview

## Purpose

Desk_items was built as a focused computer-vision demonstration for a
potential commercial cleaning-robot application.

A commercial cleaning company deploys robots to clean office
environments. The robot needs to recognize common objects that may
appear on desks and in offices.

## Engineering objective

Build a detector that is:

-   accurate enough to demonstrate useful object detection
-   lightweight enough to be a plausible onboard candidate
-   fast enough to investigate real-time deployment
-   robust to ordinary office variation
-   practical to build quickly with Roboflow

## Final classes

1.  Charger
2.  Computer
3.  Mouse
4.  Mug
5.  Notebook
6.  Pen

## Proposed project targets

These are project-specific acceptance targets, not universal industry
standards:

-   Recall ≥ 90%
-   mAP@50 ≥ 90%
-   Precision ≥ 90%
-   F1 ≥ 90%
-   mAP@50:95 ≥ 70%
-   Latency ≤ 10 ms\*
-   Real-time ≥ 30 FPS\*

Recall received slightly higher operational priority because missed real
objects can matter to a cleaning robot.

\* Final latency/FPS must ultimately be measured on the target robot
hardware.

## Scope

The work covered image collection, HEIC conversion, annotation, dataset
versioning, training, architecture comparison, annotation cleanup,
augmentation testing, targeted data expansion, local self-hosted
inference, batch inference, and live webcam inference.

## Final outcome

The final selected configuration was RF-DETR Small without augmentation,
using the V8 targeted-data-expansion dataset. The model was successfully
connected to a locally hosted Roboflow inference server and demonstrated
with an Insta360 Link 2 webcam.

# Experiment Log

## V1 --- `v1 - baseline everything`

Purpose: establish the initial Roboflow object-detection workflow.

-   163 images
-   100% train / 0% validation / 0% test
-   Auto-Orient
-   Fit within 512×512
-   No augmentation

Decision: move to a proper train/validation/test split.

## V2 --- `v2 - model definition`

Question: Does a reasonable RF-DETR Small model work?

Configuration:

-   163 images
-   70/20/10 split
-   RF-DETR Small
-   `desk_items-2-rfdetr-small-t1`
-   512×512
-   No augmentation

Results:

-   mAP@50: 92.9%
-   Precision: 93.7%
-   Recall: 86.1%
-   F1: 89.5%
-   Optimal confidence: 50%
-   Cloud API latency: 4.4 ms

Evaluation identified Pen false negatives, Notebook/Pen confusion,
limited Mug representation, and only 16 test images.

Decision: keep RF-DETR Small and target the observed data weaknesses.

## V3 --- `v3 - added targeted i...`

Question: Can additional labeled images address the V2 weaknesses?

Action: added and labeled targeted images around Pen, Mug, Pen/Notebook
distinction, and realistic desk scenes.

Dataset reached 241 images.

Results:

-   mAP@50: 90.5%
-   mAP@75: 77.0%
-   mAP@50:95: 70.3%
-   Precision: 88.6%
-   Recall: 83.8%
-   F1: 85.7%
-   Median serverless latency: 4.2 ms

Meaning: additional data did not automatically improve the aggregate
score on the new evaluation configuration. It demonstrated why image
count alone is not a sufficient success criterion.

## V4 --- `v3-updated bounding bo...`

Question: Does annotation quality improve the same model?

Action:

-   removed partial/fragmented boxes
-   tightened boxes
-   applied stricter bounding-box tolerances
-   kept RF-DETR Small

Results:

-   mAP@50: 93.2%
-   mAP@75: 80.1%
-   mAP@50:95: 76.7%
-   Precision: 96.0%
-   Recall: 87.0%
-   F1: 91.1%
-   Optimal confidence: 49%
-   Median serverless latency: 4.9 ms

Meaning: mAP@50:95 increased 6.4 points versus V3, consistent with
cleaner labels improving localization and detection quality.

Decision: treat annotation quality as a major lever.

## V5 --- `v3- yolo`

Question: Is a different detector family materially better?

Results:

-   mAP@50: 63.2%
-   Precision: 61.2%
-   Recall: 61.5%
-   F1: 60.2%
-   Latency: 4.2 ms

Meaning: the tested YOLO configuration was substantially worse, while
the latency advantage was only about 0.7 ms versus V4.

Decision: continue with RF-DETR.

Qualification: this establishes the result for the tested YOLO
configuration; it does not establish that YOLO models are universally
inferior.

## V6 --- `v4- DETR large`

Question: Does more model capacity improve results?

RF-DETR Large results:

-   mAP@50: 92.7%
-   Precision: 90.8%
-   Recall: 87.1%
-   Latency: 4.5 ms

Meaning: more capacity did not provide a meaningful improvement. Medium
was considered but skipped to save time.

Decision: keep RF-DETR Small.

## V7 --- `v5 - dete small w aug`

Question: Does augmentation improve robustness enough to justify its
cost?

Augmentation:

-   horizontal flip
-   rotation -15° to +15°
-   grayscale on 15% of images
-   brightness -15% to +15%
-   blur 2.5 px
-   2× augmentation multiplier

Results:

-   mAP@50: 93.4%
-   Precision: 92.1%
-   Recall: 87.1%
-   Latency: 5.1 ms
-   Optimal confidence: 51%

Meaning: only +0.2 mAP@50, while precision fell and latency increased.

Decision: no augmentation in the final configuration.

## V8 --- `v6 - targeted data expansion w known model`

Question: Can targeted additional data improve generalization while
retaining the known best configuration?

Dataset:

-   292 images
-   200 train / 48 validation / 44 test
-   20 office-environment images explicitly held out in Test
-   no augmentation

Model:

`desk_items-8-rfdetr-small-t1`

Results:

-   mAP@50: 93.0%
-   mAP@75: 78.2%
-   mAP@50:95: 76.9%
-   Precision: 91.6%
-   Recall: 87.6%
-   F1: 89.5%
-   Optimal confidence: 48%
-   Median serverless latency: 4.9 ms across 44 test requests

Decision: stop tuning and move to deployment.

## Decision path

``` text
V2 baseline
   ↓
V2 failure analysis
   ↓
V3 targeted data expansion
   ↓
V4 annotation cleanup
   ↓
V5 YOLO comparison
   ↓
V6 larger RF-DETR
   ↓
V7 augmentation
   ↓
V8 targeted expansion
   ↓
RF-DETR Small / no augmentation
   ↓
Local deployment
```

## Main lesson

The strongest practical improvement came from observing failure modes,
improving data quality/relevance, testing alternatives, measuring
tradeoffs, and stopping when the accuracy/speed tradeoff became clear.

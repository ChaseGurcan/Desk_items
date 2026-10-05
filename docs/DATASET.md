# Dataset Documentation

## Final dataset

-   292 images
-   6 classes
-   0 unannotated images
-   200 train
-   48 validation
-   44 test

The final split was approximately 68/16/16. This differs from a standard
random split because 20 new office-environment images were explicitly
placed in Test to evaluate generalization to an unseen environment.

## Evolution

### V1

-   163 images
-   100% train
-   Auto-Orient
-   Fit within 512×512
-   No augmentation

This established the initial workflow but did not provide a meaningful
validation/test design.

### V2

-   163 images
-   114 train / 33 validation / 16 test
-   70/20/10
-   RF-DETR Small
-   No augmentation

Evaluation identified Pen false negatives, Notebook/Pen confusion,
limited Mug representation, and an undersized test set.

### V3 targeted expansion

Additional images were collected and labeled specifically to target
inefficiencies identified in V2, including Pen detection, Mug
representation, Pen/Notebook distinction, and realistic desk scenes.

The dataset reached 241 images.

### V4 annotation cleanup

Partial/fragmented boxes were removed and stricter bounding-box
tolerances were applied. Boxes were made tighter and more consistent.

### Later expansion

27 additional images were annotated with Astra-6 AI assistance and then
manually reviewed/corrected.

Separately, 24 generic office-environment images were collected. Twenty
were explicitly assigned to Test only.

The final dataset reached 292 images.

## Annotation rules

-   One coherent bounding box per physical object.
-   Tight boxes rather than unnecessary background.
-   Separate boxes for separate instances.
-   Annotate clearly identifiable objects when enough visible area
    establishes a meaningful box.
-   Do not invent hidden boundaries.
-   Avoid fragmented/disconnected boxes.
-   Tiny fragments with unknown full extent may remain unannotated.
-   Edge-of-frame objects may be annotated.
-   Images with none of the six target classes may remain in the
    dataset.

## AI-assisted annotation

Astra-6 was used for 27 images as an annotation-speed experiment:

``` text
AI annotation
    ↓
Human review
    ↓
Correction
    ↓
Final labels
```

AI output was not treated as ground truth.

## Holdout principle

The 20 office-environment images were intended as a final exam for
generalization. They should not be used to tune the model unless the
evaluation strategy is intentionally changed and documented.

## GitHub storage

Do not commit the raw 292-image dataset. GitHub should contain the
dataset documentation, not the full image collection.

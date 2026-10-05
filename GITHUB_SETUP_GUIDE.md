# GitHub Setup Guide

## 1. Put the project in one local folder

I recommend:

```bash
mkdir -p ~/desk_items
cd ~/desk_items
```

Copy your source files and this documentation into that folder.

Recommended structure:

```text
desk_items/
├── README.md
├── .gitignore
├── requirements.txt
├── LICENSE
├── docs/
├── src/
├── scripts/
├── configs/
├── results/
└── presentations/
```

## 2. Do NOT copy these

Do not put these in the repository:

- `.venv/`
- raw image datasets
- `.heic` / `.mov` source files
- API keys
- model caches
- large generated inference-output directories

Your `.gitignore` is already configured for the main cases.

## 3. Initialize Git

```bash
cd ~/desk_items
git init
git branch -M main
```

## 4. Inspect before committing

```bash
git status
```

You want to see your documentation and source code.

If you see an API key, raw images, or `.venv/`, stop and fix it before continuing.

## 5. First commit

```bash
git add README.md docs/ src/ scripts/ configs/ results/ requirements.txt LICENSE .gitignore
git status
git commit -m "Initial Desk_items project documentation and deployment"
```

## 6. Create the GitHub repository

On GitHub:

1. Click **New repository**.
2. Name it `desk_items`.
3. Add a description such as:

```text
Roboflow object-detection project for a commercial office-cleaning robot use case.
```

4. Choose Public if you want this as a portfolio project.
5. Do not create another README on GitHub because you already have one locally.

## 7. Connect the local repo

GitHub will show the repository URL.

SSH example:

```bash
git remote add origin git@github.com:YOUR_USERNAME/desk_items.git
```

HTTPS example:

```bash
git remote add origin https://github.com/YOUR_USERNAME/desk_items.git
```

Verify:

```bash
git remote -v
```

## 8. Push

```bash
git push -u origin main
```

Refresh GitHub.

## 9. Add your actual source code

Place the final deployment scripts in:

```text
src/webcam.py
src/run_all_images.py
src/test_workflow.py
```

and the HEIC conversion script in:

```text
scripts/convert_heic.py
```

Then:

```bash
git add src/ scripts/
git commit -m "Add local inference and preprocessing scripts"
git push
```

## 10. Add presentations

Put final presentation files in:

```text
presentations/
```

For example:

```text
presentations/
├── Desk_items_CSuite_Executive_Deck_FINAL_LIGHT.pptx
├── Desk_items_Procedure_and_Architecture_Summary_with_V3.pptx
└── Desk_items_Roboflow_Project_Theme_Updated.pptx
```

## 11. Normal future workflow

After making changes:

```bash
git status
git diff
git add .
git status
git commit -m "Describe the change"
git push
```

## 12. Secret safety

Never commit:

```text
ROBOFLOW_API_KEY
```

Your local workflow should continue to use:

```bash
export ROBOFLOW_API_KEY='YOUR_CURRENT_ROBOFLOW_API_KEY'
```

If a key is ever accidentally committed, rotate the key immediately. Removing it in a later commit does not make the exposed key safe.

## 13. What the finished GitHub repo should communicate

A reviewer should be able to follow:

```text
Customer problem
      ↓
Dataset creation
      ↓
Annotation
      ↓
Experiments
      ↓
Model selection
      ↓
Architecture
      ↓
Local deployment
      ↓
Source code
```

That is the main value of this repository: it shows the engineering decision process, not merely a trained model.

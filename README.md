# Sports Certificate NER Pipeline

A production-style Natural Language Processing project that extracts structured fields from unstructured sports certificate text using a hybrid NER architecture.

This repository demonstrates end-to-end ML engineering: data transformation, model training, API orchestration, inference, artifact management, and logging.

## Why This Project Matters

Sports certificates are often written in natural language.
To use that data in dashboards, CRMs, scholarship systems, or analytics pipelines, the text must be normalized into structured fields.

This project solves that with a hybrid NER strategy:
- `spaCy custom NER` for domain-specific fields.
- `BERT (dslim/bert-base-NER)` for participant name extraction.

The final output is tabular and directly usable for downstream automation.

## Table of Contents

1. Project Overview
2. Business Use Cases
3. Key Features
4. System Architecture
5. End-to-End Workflow
6. Repository Structure
7. Module-by-Module Breakdown
8. Data Contracts and Formats
9. Entity Extraction Design
10. Training Pipeline Deep Dive
11. Inference Pipeline Deep Dive
12. API Endpoints
13. Local Setup and Installation
14. Run Instructions
15. Example Prediction Walkthrough
16. Artifacts and Logs
17. Engineering Decisions
18. Known Limitations
19. Improvement Roadmap
20. Troubleshooting
21. Resume-Ready Highlights
22. Tech Stack
23. References

## 1. Project Overview

The goal is to convert free-form sports certificate descriptions into structured attributes:
- Participant name
- Sport name
- Winning position
- Organization year

The system combines two models:
- A custom-trained spaCy NER model for `SPORTS_NAME`, `WINNING_POSITION`, and `ORG_YEAR`.
- A pre-trained BERT NER model for person entities (`B-PER`, `I-PER`).

Output is exported to Excel for easy business usage.

## 2. Business Use Cases

- Certificate digitization for schools and academies
- Candidate profile enrichment for scholarship portals
- Sports performance analytics datasets
- Event participation record normalization
- Bulk extraction for administrative back-office teams

## 3. Key Features

- End-to-end train pipeline orchestrated in code
- JSON annotation to spaCy binary conversion (`.spacy`)
- Custom NER training with configurable spaCy config
- Hybrid inference (spaCy + BERT)
- FastAPI endpoint to trigger training
- Excel-based input and output workflow
- Structured logging and artifact directories

## 4. System Architecture

The architecture is intentionally modular:

1. `DataTransformation` component
Converts labeled JSON into spaCy `DocBin` files.

2. `ModelTraining` component
Runs `spacy init config` and `spacy train` commands.

3. `TrainPipeline` orchestrator
Executes transformation then training in sequence.

4. `ModelPredictor`
Loads trained spaCy model and pre-trained BERT model.

5. `FastAPI app`
Exposes a route to launch training from an HTTP call.

## 5. End-to-End Workflow

1. Annotated JSON files are prepared in `data/`.
2. Train and test annotations are loaded.
3. Text and entities are transformed to spaCy binary format.
4. Artifacts are written under `artifacts/DataTransformationArtifacts/`.
5. spaCy config is generated and used for model training.
6. Trained model artifacts are written under `artifacts/ModelTrainerArtifacts/`.
7. For inference, pending certificate text is loaded from Excel.
8. spaCy extracts sports fields and year.
9. BERT extracts participant names.
10. Combined output is written into `output.xlsx`.

## 6. Repository Structure

```text
ner_project/
|-- app.py
|-- prediction.py
|-- requirements.txt
|-- setup.py
|-- README.md
|-- data.txt
|-- __init__.py
|-- .gitignore
|-- config/
|   `-- config.cfg
|-- data/
|   `-- data.xlsx
|-- artifacts/
|   |-- DataTransformationArtifacts/
|   `-- logs/
|       `-- ner.log
|-- report/
|   `-- Report.pdf
|-- research/
|   |-- config.cfg
|   |-- demo.ipynb
|   `-- sports_ner.ipynb
`-- src/
    |-- __init__.py
    |-- components/
    |   |-- __init__.py
    |   |-- data_transformation.py
    |   `-- model_training.py
    |-- constant/
    |   `-- __init__.py
    |-- entity/
    |   |-- __init__.py
    |   |-- artifacts_entity.py
    |   `-- config_entity.py
    |-- exception/
    |   `-- __init__.py
    |-- pipeline/
    |   |-- __init__.py
    |   `-- train_pipeline.py
    `-- utils/
        |-- __init__.py
        `-- main_utils.py
```

## 7. Module-by-Module Breakdown

### `app.py`
- Creates FastAPI app.
- Configures CORS.
- Exposes `GET /train` to run the full training pipeline.

### `prediction.py`
- Loads BERT tokenizer and model from Hugging Face.
- Loads trained spaCy model from artifacts.
- Reads pending descriptions from Excel sheet `Data-Pending`.
- Writes extracted entities into `output.xlsx`.

### `src/components/data_transformation.py`
- Reads annotation JSON files.
- Builds `DocBin` objects with entity spans.
- Saves `train_data.spacy` and `test_data.spacy`.

### `src/components/model_training.py`
- Creates model-training artifact directory.
- Executes spaCy CLI commands for config and training.
- Produces model artifacts in output directory.

### `src/pipeline/train_pipeline.py`
- Orchestrates component execution order.
- Handles top-level pipeline control flow.

### `src/entity/*`
- Defines typed config and artifact dataclasses.
- Keeps path contracts centralized and explicit.

### `src/constant/__init__.py`
- Central place for directory/file constants.

### `src/exception/__init__.py`
- Custom exception wrapper with filename and line number context.

### `src/utils/main_utils.py`
- Utility helper for JSON reading.

## 8. Data Contracts and Formats

### 8.1 Annotation JSON Contract

The transformation step expects annotation files with this structure:

```json
{
  "annotations": [
    [
      "Sample certificate sentence",
      {
        "entities": [
          [10, 22, "SPORTS_NAME"],
          [40, 52, "WINNING_POSITION"],
          [60, 64, "ORG_YEAR"]
        ]
      }
    ]
  ]
}
```

Expected file paths:
- `data/train_annotations.json`
- `data/test_annotations.json`

### 8.2 Inference Input Contract

`prediction.py` expects:
- Excel file path: `data/data.xlsx`
- Sheet name: `Data-Pending`
- One certificate description per row

### 8.3 Inference Output Contract

Generated file:
- `output.xlsx`

Output columns:
- `Certificate Description`
- `participent_name`
- `sports_name`
- `winning_position`
- `org_year`

Note: `participent_name` is spelled as implemented in current code.

## 9. Entity Extraction Design

Custom labels handled by spaCy:
- `SPORTS_NAME`
- `WINNING_POSITION`
- `ORG_YEAR`

Person extraction handled by BERT:
- `B-PER`
- `I-PER`

Rationale:
- Domain entities are better captured by custom task-specific training.
- Person entities benefit from transfer learning using a pre-trained NER model.

## 10. Training Pipeline Deep Dive

The training route (`GET /train`) triggers:

1. Data transformation init
2. Annotation JSON loading
3. Conversion to spaCy binary format
4. Artifact folder creation
5. spaCy config generation command
6. spaCy train command execution
7. Model artifact persistence

Important files used:
- `config/config.cfg`
- `artifacts/DataTransformationArtifacts/train_data.spacy`
- `artifacts/DataTransformationArtifacts/test_data.spacy`

## 11. Inference Pipeline Deep Dive

`ModelPredictor.initiate_model_predictor()` performs:

1. Load tokenizer from `dslim/bert-base-NER`
2. Load token classification model from same checkpoint
3. Load trained spaCy model from `artifacts/ModelTrainerArtifacts/model-best`
4. Read pending certificate descriptions from Excel
5. Run spaCy extraction for sports fields and year
6. Run BERT extraction for participant names
7. Merge predictions and export to Excel

## 12. API Endpoints

### `GET /train`

Purpose:
- Trigger full training pipeline.

Success response:
- `Training successful !!`

Error response:
- `Error Occurred! <message>`

## 13. Local Setup and Installation

### 13.1 Prerequisites

- Python 3.10+ recommended
- Internet connection for first-time Hugging Face model download
- Adequate RAM for spaCy and transformer loading

### 13.2 Clone and Install

```bash
git clone <your-repo-url>
cd ner_project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 14. Run Instructions

### 14.1 Run Training Through API

```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

Then call:

```bash
curl http://127.0.0.1:8080/train
```

### 14.2 Run Prediction Script

```bash
python prediction.py
```

After completion, check:
- `output.xlsx`

## 15. Example Prediction Walkthrough

Sample input sentence:

```text
Ravi Kumar secured 1st Position in Basketball during 2012 championship.
```

Expected structured extraction pattern:

```text
participent_name: Ravi Kumar
sports_name: Basketball
winning_position: 1st Position
org_year: 2012
```

## 16. Artifacts and Logs

Artifacts directory behavior:
- Created automatically during runtime.
- Stores transformed data and trained model outputs.

Log file:
- `artifacts/logs/ner.log`
- Contains pipeline progress and error traces.

## 17. Engineering Decisions

- Chose modular components for maintainability.
- Centralized constants for predictable path handling.
- Used dataclasses for explicit config contracts.
- Separated training orchestration from component logic.
- Used FastAPI for simple operational trigger surface.

## 18. Known Limitations

- No dedicated prediction API route yet (prediction is script-based).
- Annotation files are expected but not bundled by default.
- Current implementation is oriented to English text templates.
- End-to-end tests are not currently included.

## 19. Improvement Roadmap

1. Add `POST /predict` endpoint with JSON payload support.
2. Add unit tests for transformation and extraction modules.
3. Add Docker support for one-command deployment.
4. Add CI pipeline for lint, test, and packaging checks.
5. Add model evaluation report generation (precision/recall/F1).
6. Replace `os.system` calls with subprocess and exit-code handling.
7. Add strict schema validation for input annotation files.
8. Add batch inference API with async job tracking.

## 20. Troubleshooting

Issue: `train_annotations.json` not found.
- Fix: place annotation files inside `data/` with expected names.

Issue: spaCy model loading fails in prediction.
- Fix: ensure training completed and `model-best` exists in artifacts.

Issue: Hugging Face download errors.
- Fix: verify internet connectivity and proxy/firewall settings.

Issue: Empty extraction fields.
- Fix: validate training label quality and sentence diversity.

## 21. Resume-Ready Highlights

Use the following points directly in your resume or interview:

- Built a hybrid NER engine combining custom spaCy training and transformer-based person extraction.
- Designed modular ML pipeline architecture with transformation, training, and inference layers.
- Implemented API-driven training orchestration using FastAPI for operational simplicity.
- Developed artifact and logging conventions for reproducibility and debugging.
- Delivered structured Excel output from unstructured certificate narratives.

## 22. Tech Stack

Languages and runtime:
- Python

ML and NLP:
- spaCy
- Hugging Face Transformers
- PyTorch

Data and I/O:
- pandas
- openpyxl

API and serving:
- FastAPI
- Uvicorn

Utilities:
- tqdm

## 23. References

- spaCy docs: https://spacy.io/usage
- Hugging Face model: https://huggingface.co/dslim/bert-base-NER
- FastAPI docs: https://fastapi.tiangolo.com/

---

If you are evaluating this project as a recruiter:
this repository showcases practical applied NLP engineering, clear modular design, and deployable workflow thinking beyond notebook-level experimentation.

# Fraud Detection API

## Tags

`machine-learning` `fraud-detection` `lightgbm` `fastapi` `shap` `docker` `api` `mlops`

---

## Description

A production-ready **Fraud Detection REST API** built with **FastAPI** and **LightGBM**, supporting real-time predictions and **SHAP-based explainability**. The API is designed for deployment using **Docker**, follows ML serving best practices, and includes automated CI via **GitHub Actions**.

The model was trained on engineered PCA-based transaction features and exposes two main endpoints:

* `/predict` – fraud probability and classification
* `/explain` – per-feature SHAP explanations

---

## Tech Stack

* **Python 3.10**
* **FastAPI** – API framework
* **LightGBM** – fraud classification model
* **SHAP** – model explainability
* **scikit-learn** – preprocessing
* **Docker & Docker Compose** – containerization
* **GitHub Actions** – CI pipeline

---

## Project Structure

```
fraud-detection-api/
├── app/
│   ├── main.py
│   ├── predict.py
│   ├── explain.py
│   ├── model_loader.py
│   └── schemas.py
├── models/
│   ├── lgbm_tuned.pkl
│   ├── scaler.pkl
│   └── lgbm_metadata.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## API Endpoints

### POST /predict

Predict whether a transaction is fraudulent.

**Request**

```json
{
  "V1": -1.23,
  "V2": 0.45,
  "V3": -0.67,
  "Amount": 120.5,
  "Time": 35000
}
```

**Response**

```json
{
  "fraud_probability": 0.0342,
  "prediction": 0
}
```

---

### POST /explain

Return SHAP values explaining the fraud prediction.

**Response**

```json
{
  "V1": -0.021,
  "V2": 0.013,
  "Amount_scaled": 0.004
}
```

---

## Running Locally (Without Docker)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Docker Setup

### Dockerfile

The API is containerized using Python 3.10 slim and includes system dependencies required by LightGBM.

---

### Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: "3.9"

services:
  fraud-api:
    build: .
    container_name: fraud-detection-api
    ports:
      - "8000:8000"
    restart: unless-stopped
```

### Run with Docker Compose

```bash
docker-compose up --build
```

---

## GitHub Actions (CI)

Create `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint check
        run: |
          pip install flake8
          flake8 app --max-line-length=100

      - name: Docker build
        run: docker build -t fraud-detection-api .
```

---

## Deployment Ready

This API is ready to be deployed on:

* AWS EC2 / ECS
* Google Cloud Run
* Azure Container Apps
* Any Docker-compatible platform

---

## License

MIT License

---

## Author

Saint Yves

---

## Status

✔ Model loaded at startup
✔ Deterministic feature alignment
✔ Explainability enabled
✔ Dockerized
✔ CI enabled

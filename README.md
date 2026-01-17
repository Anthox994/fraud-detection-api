# Fraud Detection API

## Overview

This project is a **production‑ready Fraud Detection REST API** built with **FastAPI** and a **LightGBM binary classifier**, designed to score financial transactions for fraud risk and provide **model explainability using SHAP**. A continuation of my previous project [credit_card_fraud_detection_system_for_credit_card_transactions](https://github.com/SaintJeane/credit_card_fraud_detection_system_for_credit_card_transactions), where the best trained model, and the model's metadata are retrieved from for deployment.

The system exposes endpoints for:

* Fraud probability prediction
* Local, per‑transaction explainability (top contributing features)
* Health and readiness checks

The application is fully **Dockerized**, uses **strict request/response schemas**, and follows best practices for **ML inference APIs**.

---

## Key Features

* ⚡ FastAPI for high‑performance inference
* 🌲 LightGBM binary classification model
* 🔍 SHAP‑based explainability (TreeExplainer)
* 📦 Docker & Docker Compose support
* 🧪 Input validation with Pydantic
* 🩺 Health and startup checks
* 🧾 Structured logging

---

## Project Structure

```text
fraud-detection-api/
├── app/
│   ├── main.py                 # FastAPI app & routes
│   ├── predict.py              # Prediction logic
│   ├── explain.py              # SHAP explainability logic
│   ├── schemas.py              # Pydantic schemas
│   ├── model_loader.py         # Model, scaler, metadata loading
│   ├── feature_descriptions.py # Helper for feature descriptions mapping
|   ├── logging_config.py 
│   └── __init__.py
├── models/
│   ├── lgbm_tuned.pkl
│   ├── scaler.pkl
│   └── lgbm_metadata.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Model Details

* **Algorithm**: LightGBM (binary classifier)
* **Output**: Fraud probability + threshold‑based prediction
* **Threshold**: Loaded from model metadata
* **Features**:

  * PCA components: `V1` … `V28`
  * Engineered features: `Amount_scaled`, `Time_scaled`

All inference inputs are internally aligned to the exact feature set used during training.

---

## API Endpoints

### `POST /predict`

Predicts fraud probability for a transaction.

An example of an input data:

**Request Body**

```json
{
  "data": {
    "V1": -1.23,
    "V2": 0.45,
    "V3": -0.67,
    "Amount": 120.5,
    "Time": 35000
  }
}
```

**Response**

```json
{
  "fraud_probability": 0.0123,
  "prediction": 0
}
```

---

### `POST /explain`

Returns SHAP‑based explanations for a transaction.

**Request Body**

```json
{
  "data": {
    "V1": -1.23,
    "V2": 0.45,
    "V3": -0.67,
    "Amount": 120.5,
    "Time": 35000
  }
}
```

**Response**

```json
{
  "fraud_probability": 0.0123,
  "top_features": [
    {
      "feature": "V14",
      "description": "Transaction risk signal",
      "shap_value": 0.345678,
      "impact": "increases fraud risk"
    }
  ]
}
```

---

### `GET /health`

Health check endpoint.

**Response**

```json
{
  "status": "ok"
}
```

---

## Running Locally

### 1. Clone Repository

```bash
git clone https://github.com/SaintJeane/fraud-detection-api.git
cd fraud-detection-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run API

```bash
uvicorn app.main:app --reload
```

Open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Running with Docker

### Build Image

```bash
docker build -t fraud-detection-api .
```

### Run Container

```bash
docker run -p 8000:8000 fraud-detection-api
```

---

## Running with Docker Compose

```bash
docker compose up --build
```

Stop services:

```bash
docker compose down
```

---

## Explainability Notes

* SHAP values are computed using `TreeExplainer`
* Binary classification output is normalized to handle SHAP API changes
* Only top‑K most impactful features are returned
* All SHAP values are JSON‑safe floats

---

## Tech Stack

* Python 3.10
* FastAPI
* LightGBM
* SHAP
* Pandas / NumPy
* Docker & Docker Compose

---

## Tags

`fastapi` `machine-learning` `fraud-detection` `lightgbm` `shap` `ml-api` `docker`

---

## License

MIT License

---

## Disclaimer⚠️

This project is for educational and demonstrative purposes. It should not be used as‑is for real‑world financial decision‑making without additional validation, monitoring, and compliance controls.

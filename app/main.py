'''FasTAPI entry point'''

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from .schemas import Transaction, PredictionResponse, ExplainResponse
from .predict import predict_transaction
from .explain import explain_transaction
from .model_loader import model, scaler, FEATURES

# Validate model & scaler at startuo
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup validation (runs before app starts)
    assert model is not None, "Model failed to load"
    assert scaler is not None, "Scaler failed to load"
    assert FEATURES is not None and len(FEATURES) > 0, "Features not loaded"
    yield # app runs here
    # Optional: Add cleanup code here for shutdown
    
# Create app with lifespan handler
app = FastAPI(
    lifespan=lifespan,
    title="Credit Card Fraud Detection API",
    description="LightGBM-based fraud detection with explainability",
    version="1.0"
)

    
# health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok",
            "service": "fraud-detection-api"}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(tx: Transaction):
    return predict_transaction(tx.data)

# Explainability endpoint
@app.post("/explain", response_model=ExplainResponse)
async def explain(tx: Transaction):
    try:
        return explain_transaction(tx.data)
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
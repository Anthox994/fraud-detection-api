'''
Model loading and prediction logic 
single source of truth for model & metadata
'''
import joblib
import json
from pathlib import Path

# Setting up file paths
BASE_DIR = Path(__file__).resolve().parent.parent # root directory

MODEL_PATH = BASE_DIR / "models" / "lgbm_tuned.pkl"
METADATA_PATH = BASE_DIR / "models" / "lgbm_metadata.json"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"
FEATURES_PATH = BASE_DIR / "models" / "features.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
# FEATURES = joblib.load(FEATURES_PATH)

with open(METADATA_PATH) as f:
    metadata = json.load(f)
    
FEATURES = metadata["features"]
THRESHOLD = metadata["threshold"]
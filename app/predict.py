'''Prediction logic'''

import pandas as pd
from .model_loader import model, FEATURES, THRESHOLD, scaler
from .logging_config import logger

def predict_transaction(transaction: dict):
    logger.info("Received prediction request")
    
    # Initiate all features to 0
    data = {feature: 0.0 for feature in FEATURES}
    
    # Update with provided values
    for key, value in transaction.items():
        if key in data:
            data[key] = value
             
    # Apply scaling if needed
    if "Amount" in transaction:
        data["Amount_scaled"] = scaler.transform(
            [[transaction["Amount"]]]
        )[0][0]
        
    if "Time" in transaction:
        data["Time_scaled"] = scaler.transform(
            [[transaction["Time"]]]
        )[0][0]
    
    # Create a DataFrame in correct feature order        
    X = pd.DataFrame([[data[f] for f in FEATURES]], columns=FEATURES)
        
    # Predict
    # proba = model.predict_proba(X)[:, 1][0]
    # proba = model.predict_proba(X)[:, 1]
    proba = model.predict_proba(X)[0, 1]
    prediction = int(proba >= THRESHOLD)
    
    logger.info(
        "Prediction completed | probability=%s | prediction=%s",
        round(float(proba), 4),
        prediction
    )
    
    return {
        "fraud_probability": round(float(proba), 4),
        "prediction": prediction
    }
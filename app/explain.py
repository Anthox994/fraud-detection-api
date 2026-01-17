'''SHAP explanations'''

import shap
import pandas as pd
from .model_loader import model, FEATURES, scaler
from .feature_descriptions import FEATURE_DESCRIPTIONS
import warnings

warnings.filterwarnings("ignore", 
                        message=".*LightGBM binary classifier with TreeExplainer shap values output has changed.*", 
                        category=UserWarning,)

TOP_K = 5 # Configurable

explainer = shap.TreeExplainer(model)

def explain_transaction(transaction: dict):
    # Build full feature vector
    data = {feature: 0.0 for feature in FEATURES}
    
    for key, value in transaction.items():
        if key in data:
            data[key] = value
    
    # Apply scaling
    if "Amount" in transaction:
        data["Amount_scaled"] = scaler.transform(
            [[transaction["Amount"]]]
            )[0][0]
        
    if "Time" in transaction:
        data["Time_scaled"] = scaler.transform(
            [[transaction["Time"]]]
            )[0][0]
        
    X = pd.DataFrame([[data[f] for f in FEATURES]], columns=FEATURES)
    
    # Prediction probability
    fraud_proba = model.predict_proba(X)[0][1]
        
    # SHAP values (fraud class)
    shap_values = explainer.shap_values(X)
    
    #    
    if isinstance(shap_values, list):
        # Binary classifier with 2 outputs
        shap_row = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
    else:
        # Binary classifier with single output
        shap_row = shap_values[0]    
        
    # Build explanation objects
    explanations = []
    
    for feature, value in zip(FEATURES, shap_row):
        explanations.append({
            "feature" : feature,
            "description" : FEATURE_DESCRIPTIONS.get(feature, feature),
            "shap_value" : round(float(value), 6),
            "abs_value" : abs(float(value)),
            "impact" : (
                "increases fraud risk" if value > 0 else "decreases fraud risk"
            )
        })
    
    # Sort & select top-k
    explanations = sorted(
        explanations,
        key=lambda x: x["abs_value"],
        reverse=True
    )[:TOP_K]
    
    # Remove helper field
    for e in explanations:
        e.pop("abs_value")
    
    return {
        "fraud_probability": round(float(fraud_proba), 6),
        "top_features": explanations
    } 
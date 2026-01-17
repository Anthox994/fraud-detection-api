'''
Input/output validation
'''
from pydantic import BaseModel
from typing import Dict, Optional, List

# Defining the input schema
class Transaction(BaseModel):
    data: Dict[str, float]

# Defining the output schema    
class PredictionResponse(BaseModel):
    fraud_probability: float
    prediction: int
    
# Defining an explicit response schema for explain
class FeatureExplanation(BaseModel):
    feature: str
    description: str
    shap_value: float
    impact: str

class ExplainResponse(BaseModel):
    fraud_probability: float
    top_features: List[FeatureExplanation]
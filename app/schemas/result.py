from pydantic import BaseModel
from typing import List, Union
from datetime import datetime

class AlzheimerResult(BaseModel):
    test_type: str = "alzheimer_model"
    diagnosis: str
    probability: float
    risk_level: str

class CognitiveResult(BaseModel):
    test_type: str = "cognitive_model"
    score: float
    level: str

class TestResultSchema(BaseModel):
    patient_id: str
    results: List[Union[AlzheimerResult, CognitiveResult]]
    timestamp: datetime

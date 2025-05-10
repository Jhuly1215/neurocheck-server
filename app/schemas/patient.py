from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4


class PatientSchema(BaseModel):
    patient_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    age: int
    gender: str
    ethnicity: Optional[str]
    education_level: Optional[str]
    bmi: Optional[float]
    smoking: Optional[bool]
    alcohol_consumption: Optional[bool]
    physical_activity: Optional[str]
    diet_quality: Optional[str]
    sleep_quality: Optional[str]
    family_history_alzheimers: Optional[bool]
    cardiovascular_disease: Optional[bool]
    diabetes: Optional[bool]
    depression: Optional[bool]
    head_injury: Optional[bool]
    hypertension: Optional[bool]
    systolic_bp: Optional[int]
    diastolic_bp: Optional[int]
    cholesterol_total: Optional[float]
    cholesterol_ldl: Optional[float]
    cholesterol_hdl: Optional[float]
    cholesterol_triglycerides: Optional[float]
    mmse: Optional[int]
    functional_assessment: Optional[str]
    memory_complaints: Optional[bool]
    behavioral_problems: Optional[bool]
    adl: Optional[str]
    confusion: Optional[bool]
    disorientation: Optional[bool]
    personality_changes: Optional[bool]
    difficulty_completing_tasks: Optional[bool]
    forgetfulness: Optional[bool]
    diagnosis: Optional[str]
    doctor_in_charge: Optional[str]

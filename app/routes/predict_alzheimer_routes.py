from fastapi import APIRouter
from app.schemas.patient import PatientSchema
from app.utils.alzheimer.model_loader import get_model, get_scaler
import pandas as pd

router = APIRouter()

# Orden de columnas para el modelo
model_columns = [
    'age', 'gender', 'ethnicity', 'education_level', 'bmi', 'smoking', 'alcohol_consumption',
    'physical_activity', 'diet_quality', 'sleep_quality', 'family_history_alzheimers',
    'cardiovascular_disease', 'diabetes', 'depression', 'head_injury', 'hypertension',
    'systolic_bp', 'diastolic_bp', 'cholesterol_total', 'cholesterol_ldl', 'cholesterol_hdl',
    'cholesterol_triglycerides', 'mmse', 'functional_assessment', 'memory_complaints',
    'behavioral_problems', 'adl', 'confusion', 'disorientation', 'personality_changes',
    'difficulty_completing_tasks', 'forgetfulness'
]

def clean_input(data: PatientSchema):
    data_dict = data.dict()

    # Mapear los nombres del esquema a los que el modelo espera
    renamed = {
        "age": "Age",
        "gender": "Gender",
        "ethnicity": "Ethnicity",
        "education_level": "EducationLevel",
        "bmi": "BMI",
        "smoking": "Smoking",
        "alcohol_consumption": "AlcoholConsumption",
        "physical_activity": "PhysicalActivity",
        "diet_quality": "DietQuality",
        "sleep_quality": "SleepQuality",
        "family_history_alzheimers": "FamilyHistoryAlzheimers",
        "cardiovascular_disease": "CardiovascularDisease",
        "diabetes": "Diabetes",
        "depression": "Depression",
        "head_injury": "HeadInjury",
        "hypertension": "Hypertension",
        "systolic_bp": "SystolicBP",
        "diastolic_bp": "DiastolicBP",
        "cholesterol_total": "CholesterolTotal",
        "cholesterol_ldl": "CholesterolLDL",
        "cholesterol_hdl": "CholesterolHDL",
        "cholesterol_triglycerides": "CholesterolTriglycerides",
        "mmse": "MMSE",
        "functional_assessment": "FunctionalAssessment",
        "memory_complaints": "MemoryComplaints",
        "behavioral_problems": "BehavioralProblems",
        "adl": "ADL",
        "confusion": "Confusion",
        "disorientation": "Disorientation",
        "personality_changes": "PersonalityChanges",
        "difficulty_completing_tasks": "DifficultyCompletingTasks",
        "forgetfulness": "Forgetfulness"
    }

    # Renombrar claves
    formatted = {}
    for old_key, new_key in renamed.items():
        val = data_dict.get(old_key)
        # Convertir booleanos a enteros
        if isinstance(val, bool):
            val = int(val)
        elif val is None:
            val = 0
        formatted[new_key] = val

    return pd.DataFrame([formatted])


@router.post("/predict-alzheimer")
def predict_alzheimer(data: PatientSchema):
    model = get_model()
    scaler = get_scaler()

    input_df = clean_input(data)
    scaled_input = scaler.transform(input_df)

    # Predicción y probabilidad
    prediction = model.predict(scaled_input)[0]
    probability = round(model.predict_proba(scaled_input)[0][1] * 100, 2)
    
    diagnosis = "Alzheimer" if prediction == 1 else "No Alzheimer"

    # Nivel de riesgo
    if probability >= 80:
        risk_level = "Alto"
    elif probability >= 50:
        risk_level = "Moderado"
    else:
        risk_level = "Bajo"

    return {
        "diagnóstico": diagnosis,
        "probabilidad": f"{probability}%",
        "nivel_de_riesgo": risk_level
    }

from fastapi import APIRouter, Request
import pandas as pd
import joblib
from app.utils.dementia.model_loader import get_model, get_scaler

router = APIRouter()

# Columnas que requiere el modelo
model_columns = [
    "M/F", "Hand", "Age", "EDUC", "SES", "CDR", "eTIV", "nWBV", "ASF"
]

# Mapear campos del JSON de entrada a los del modelo
renamed = {
    "gender": "M/F",
    "hand": "Hand",
    "age": "Age",
    "education_level": "EDUC",
    "ses": "SES",
    "cdr": "CDR",
    "etiv": "eTIV",
    "nwbv": "nWBV",
    "asf": "ASF"
}

def clean_input(data: dict) -> pd.DataFrame:
    formatted = {}
    for old_key, new_key in renamed.items():
        val = data.get(old_key)
        # Manejar booleanos y valores faltantes
        if isinstance(val, bool):
            val = int(val)
        elif val is None:
            val = 0
        formatted[new_key] = val

    df = pd.DataFrame([formatted])
    df = df[model_columns]  # asegurar el orden
    return df

@router.post("/predict-dementia")
async def predict_dementia(request: Request):
    data = await request.json()

    model = get_model()
    scaler = get_scaler()

    input_df = clean_input(data)
    scaled_input = scaler.transform(input_df)

    prediction = model.predict(scaled_input)[0]
    probability = round(model.predict_proba(scaled_input)[0][1] * 100, 2)

    diagnosis = "Demencia" if prediction == 1 else "Sin demencia"

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

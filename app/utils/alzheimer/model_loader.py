import joblib

model = joblib.load('app/utils/alzheimer/modelo_alzheimer_rf_smote.pkl')
scaler = joblib.load('app/utils/alzheimer/scaler.pkl')

def get_model():
    return model

def get_scaler():
    return scaler

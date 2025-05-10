import joblib

model = joblib.load('app/utils/dementia/dementia_model.pkl')
scaler = joblib.load('app/utils/dementia/dementia_scaler.pkl')

def get_model():
    return model

def get_scaler():
    return scaler

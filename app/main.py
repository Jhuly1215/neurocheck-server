from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    patient_routes,
    answer_routes,
    result_routes,
    question_routes,
    predict_dementia_routes
)
from app.routes.predict_eeg_routes import router as predict_eeg_router
from app.routes.predict import alzheimer_routes

app = FastAPI(title="NeuroCheck API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["*"] en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas API
app.include_router(patient_routes.router, prefix="/api")
app.include_router(answer_routes.router, prefix="/api")
app.include_router(result_routes.router, prefix="/api")
app.include_router(question_routes.router, prefix="/api")
app.include_router(predict_dementia_routes.router, prefix="/api")
app.include_router(predict_eeg_router, prefix="/api")
app.include_router(alzheimer_routes.router, prefix="/api")

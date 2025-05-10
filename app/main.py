from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    patient_routes,
    answer_routes,
    predict_alzheimer_routes,
    result_routes,
    question_routes
)

app = FastAPI(title="NeuroCheck API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # o ["*"] en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas API
app.include_router(patient_routes.router, prefix="/api")
app.include_router(answer_routes.router, prefix="/api")
app.include_router(result_routes.router, prefix="/api")
app.include_router(question_routes.router, prefix="/api")
app.include_router(predict_alzheimer_routes.router, prefix="/api")

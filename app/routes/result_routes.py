from fastapi import APIRouter
from app.firebase import db
from app.schemas.result import TestResultSchema
from uuid import uuid4
from datetime import datetime
from typing import List, Dict, Any
router = APIRouter()

@router.post("/test-results/")
def save_test_result(data: TestResultSchema):
    # ID del documento basado en UUID + timestamp por claridad (puedes ajustar si lo deseas)
    doc_id = f"{data.patient_id}_{uuid4().hex}"

    # Formato para Firestore
    doc_ref = db.collection("test_results").document(doc_id)
    doc_ref.set({
        "patient_id": data.patient_id,
        "timestamp": data.timestamp.isoformat(),
        "results": [result.dict() for result in data.results]
    })

    return {"message": "Resultado del test guardado correctamente", "document_id": doc_id}

@router.get("/test-results/{patient_id}")
def get_test_results(patient_id: str):
    """
    Recupera todos los documentos de test_results para un paciente,
    ordenados por timestamp descendente.
    """
    col_ref = db.collection("test_results")
    # Filtrar por patient_id y ordenar por timestamp
    query = (
        col_ref
        .where("patient_id", "==", patient_id)
        .order_by("timestamp", direction="DESCENDING")
    )
    docs = query.stream()

    all_results: List[Dict[str, Any]] = []
    for doc in docs:
        data = doc.to_dict()
        all_results.extend(data.get("results", []))

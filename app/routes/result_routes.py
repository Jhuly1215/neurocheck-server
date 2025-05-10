from fastapi import APIRouter
from app.firebase import db
from app.schemas.result import TestResultSchema
from uuid import uuid4
from datetime import datetime

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

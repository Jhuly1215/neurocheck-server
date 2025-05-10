from fastapi import APIRouter
from app.firebase import db
from app.schemas.result import ResultBase

router = APIRouter()

@router.post("/test_results/{patient_id}")
def save_test_result(patient_id: str, data: ResultBase):
    doc_ref = db.collection("test_results").document(f"{patient_id}_{data.test_id}")
    doc_ref.set({
        "patient_id": patient_id,
        "test_id": data.test_id,
        "date": data.date,
        "irc": data.irc,
        "explanation": data.explanation,
        "report_pdf_url": data.report_pdf_url
    })
    return {"message": "Resultado del test guardado"}

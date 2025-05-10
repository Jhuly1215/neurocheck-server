from fastapi import APIRouter
from app.firebase import db
from app.schemas.answer import AnswerBase, TestResponse

router = APIRouter()

@router.post("/expected_answers/{patient_id}")
def add_expected_answer(patient_id: str, data: AnswerBase):
    doc_ref = db.collection("expected_answers").document(f"{patient_id}_{data.question_id}")
    doc_ref.set({
        "patient_id": patient_id,
        "question_id": data.question_id,
        "expected_value": data.expected_value
    })
    return {"message": "Respuesta esperada registrada"}

@router.post("/test_responses/{patient_id}")
def add_test_response(patient_id: str, data: TestResponse):
    doc_ref = db.collection("test_responses").document(f"{patient_id}_{data.question_id}")
    doc_ref.set({
        "patient_id": patient_id,
        "question_id": data.question_id,
        "answer": data.answer,
        "match": data.match,
        "color": data.color
    })
    return {"message": "Respuesta del test registrada"}

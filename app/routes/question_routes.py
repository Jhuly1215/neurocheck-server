from fastapi import APIRouter
from app.firebase import db
from app.schemas.question import QuestionSchema
from typing import List

router = APIRouter()

@router.post("/questions/bulk")
def create_questions_bulk(data: List[QuestionSchema]):
    for question in data:
        doc_ref = db.collection("questions").document(question.question_id + "_" + question.language)
        doc_ref.set(question.dict())
    return {"message": f"{len(data)} preguntas registradas"}

@router.post("/questions")
def create_question(data: QuestionSchema):
    doc_ref = db.collection("questions").document(data.question_id)
    doc_ref.set(data.dict())
    return {"message": "Pregunta registrada"}

@router.get("/questions")
def get_all_questions():
    questions = db.collection("questions").stream()
    return [doc.to_dict() for doc in questions]

@router.get("/questions/{question_id}")
def get_question(question_id: str):
    doc = db.collection("questions").document(question_id).get()
    if doc.exists:
        return doc.to_dict()
    return {"error": "Pregunta no encontrada"}

@router.delete("/questions/{question_id}")
def delete_question(question_id: str):
    db.collection("questions").document(question_id).delete()
    return {"message": "Pregunta eliminada"}

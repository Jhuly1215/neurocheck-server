from fastapi import APIRouter, HTTPException
from app.firebase import db
from app.schemas.patient import PatientSchema

router = APIRouter()

@router.post("/patients")
def create_patient(data: PatientSchema):
    doc_ref = db.collection("patients").document(data.patient_id)
    doc = doc_ref.get()
    
    if doc.exists:
        raise HTTPException(status_code=400, detail="El paciente ya existe")

    doc_ref.set(data.dict())

    return {
        "message": "Paciente registrado",
        "patient_id": data.patient_id
    }

@router.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    doc = db.collection("patients").document(patient_id).get()
    if doc.exists:
        return doc.to_dict()
    raise HTTPException(status_code=404, detail="Paciente no encontrado")

@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    db.collection("patients").document(patient_id).delete()
    return {"message": "Paciente eliminado"}

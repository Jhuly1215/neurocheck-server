from pydantic import BaseModel
from typing import Optional, List

class QuestionSchema(BaseModel):
    question_id: str
    field_name: str
    text: str                      # Pregunta en el idioma correspondiente
    response_type: str            # "boolean", "number", "text", "choice"
    options: Optional[List[str]] = None
    category: Optional[str] = None
    language: str                 # Ej. "es" para español, "ay" para aymara

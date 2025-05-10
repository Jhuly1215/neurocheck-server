from pydantic import BaseModel
from typing import Optional, Union

class AnswerBase(BaseModel):
    question_id: str
    expected_value: Optional[Union[str, int, float, bool]] = None

class TestResponse(BaseModel):
    question_id: str
    answer: str 
    match: bool
    color: str

from pydantic import BaseModel
from typing import Optional

class ResultBase(BaseModel):
    test_id: Optional[str] = "latest"
    date: str
    irc: float
    explanation: str
    report_pdf_url: Optional[str] = ""

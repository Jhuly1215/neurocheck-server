# app/schemas/eeg.py
from pydantic import BaseModel
from typing import List

class EEGDataSchema(BaseModel):
    # eeg: lista de canales, cada uno con lista de muestras
    eeg: List[List[float]]

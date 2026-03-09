"""
Pydantic response models
"""

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    msg: str
    area: int
    predicted_price: float


class PredictionRecord(BaseModel):
    id: int
    area: int
    predicted_price: float
    created_at: str

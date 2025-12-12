from pydantic import BaseModel
from typing import List, Literal

class ModelPrediction(BaseModel):
  headline: str
  source: str | None
  importance: float
  sentiment: Literal["positive", "neutral", "negative"]

class PredictRequest(BaseModel):
  stock_symbol: str

class SetModelRequest(BaseModel):
  model_name: str

class PredictResponse(BaseModel):
  data: List[dict]
  message: str
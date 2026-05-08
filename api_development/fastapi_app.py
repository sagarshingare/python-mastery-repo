"""Production-friendly API example built with FastAPI."""

from __future__ import annotations

import logging
from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="Python Mastery API", version="0.1.0")


class HealthStatus(str, Enum):
    healthy = "healthy"
    degraded = "degraded"


class PredictionRequest(BaseModel):
    feature_a: float = Field(..., description="Primary numerical feature")
    feature_b: float = Field(..., description="Secondary numerical feature")
    category: Optional[str] = Field(None, description="Optional categorical signal")


class PredictionResponse(BaseModel):
    score: float
    decision: str
    version: str


@app.get("/health", summary="Health check endpoint")
def health_check() -> dict[str, str]:
    """Return current API health status."""
    logger.info("Health check requested")
    return {"status": HealthStatus.healthy}


@app.post("/predict", response_model=PredictionResponse, summary="Predict a score from request data")
def predict(payload: PredictionRequest) -> PredictionResponse:
    """Example prediction endpoint demonstrating request validation and business logic."""
    logger.info("Received prediction request: %s", payload.dict())
    score = payload.feature_a * 0.4 + payload.feature_b * 0.6
    decision = "approve" if score >= 0.5 else "decline"
    response = PredictionResponse(score=round(score, 4), decision=decision, version="0.1.0")
    logger.info("Prediction response: %s", response.json())
    return response

"""State of Charge (SOC) prediction routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import numpy as np

from app.database import get_db
from app.models.db import Battery, SOCPrediction
from app.models.schemas import SOCPredictionResponse
from app.services.soc_service import SOCService

router = APIRouter()
soc_service = SOCService()


@router.post("/soc", response_model=SOCPredictionResponse)
async def predict_soc(
    battery_id: str,
    voltage: float,
    current: float,
    temperature: float,
    db: Session = Depends(get_db)
):
    """Predict State of Charge (SOC)"""
    # Get battery
    battery = db.query(Battery).filter(Battery.battery_id == battery_id).first()
    if not battery:
        raise Exception(f"Battery {battery_id} not found")

    # Predict SOC
    soc_value = soc_service.predict(voltage, current, temperature)

    # Store prediction
    prediction = SOCPrediction(
        battery_id=battery.id,
        timestamp=datetime.utcnow(),
        soc=soc_value,
        confidence=0.95,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return SOCPredictionResponse(
        soc=soc_value * 100,  # Convert to percentage
        confidence=0.95,
        timestamp=prediction.timestamp,
    )

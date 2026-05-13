"""State of Health (SOH) prediction routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.db import Battery, SOHPrediction
from app.models.schemas import SOHPredictionResponse
from app.services.soh_service import SOHService

router = APIRouter()
soh_service = SOHService()


@router.post("/soh", response_model=SOHPredictionResponse)
async def predict_soh(
    battery_id: str,
    cycle_count: int = 0,
    internal_resistance: float = 0.05,
    db: Session = Depends(get_db)
):
    """Predict State of Health (SOH)"""
    # Get battery
    battery = db.query(Battery).filter(Battery.battery_id == battery_id).first()
    if not battery:
        raise Exception(f"Battery {battery_id} not found")

    # Predict SOH
    soh_value = soh_service.predict(cycle_count, internal_resistance)

    # Store prediction
    prediction = SOHPrediction(
        battery_id=battery.id,
        timestamp=datetime.utcnow(),
        soh=soh_value,
        degradation_rate=0.5,  # Example: 0.5% per cycle
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return SOHPredictionResponse(
        soh=soh_value * 100,  # Convert to percentage
        timestamp=prediction.timestamp,
    )

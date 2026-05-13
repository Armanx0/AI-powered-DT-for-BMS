"""Forecasting routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.db import Battery, Forecast
from app.models.schemas import ForecastResponse
from app.services.forecast_service import ForecastService

router = APIRouter()
forecast_service = ForecastService()


@router.post("/forecast")
async def generate_forecast(
    battery_id: str,
    current_soc: float,
    current_soh: float,
    horizon_hours: int = 24,
    db: Session = Depends(get_db)
):
    """Generate multi-horizon forecast"""
    # Get battery
    battery = db.query(Battery).filter(Battery.battery_id == battery_id).first()
    if not battery:
        raise Exception(f"Battery {battery_id} not found")

    # Generate forecast
    future_soc, future_soh, future_resistance = forecast_service.forecast(
        current_soc, current_soh, horizon_hours
    )

    # Store forecast
    forecast = Forecast(
        battery_id=battery.id,
        forecast_horizon_hours=horizon_hours,
        timestamp=datetime.utcnow(),
        future_soc=future_soc.tolist() if hasattr(future_soc, 'tolist') else future_soc,
        future_soh=future_soh.tolist() if hasattr(future_soh, 'tolist') else future_soh,
        future_resistance=future_resistance.tolist() if hasattr(future_resistance, 'tolist') else future_resistance,
        confidence=0.85,
    )
    db.add(forecast)
    db.commit()

    return ForecastResponse(
        future_soc=future_soc,
        future_soh=future_soh,
        future_resistance=future_resistance,
        confidence=0.85,
        horizon_hours=horizon_hours,
        timestamp=forecast.timestamp,
    )

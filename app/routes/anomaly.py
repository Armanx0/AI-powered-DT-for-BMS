"""Anomaly detection routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.db import Battery, AnomalyLog
from app.models.schemas import AnomalyResponse
from app.services.anomaly_service import AnomalyService

router = APIRouter()
anomaly_service = AnomalyService()


@router.post("/anomaly")
async def detect_anomaly(
    battery_id: str,
    soc: float,
    soh: float,
    temperature: float,
    internal_resistance: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Detect anomalies and failures"""
    # Get battery
    battery = db.query(Battery).filter(Battery.battery_id == battery_id).first()
    if not battery:
        raise Exception(f"Battery {battery_id} not found")

    # Detect anomalies
    severity, anomaly_type, description, confidence = anomaly_service.detect(
        soc, soh, temperature, internal_resistance
    )

    # Store anomaly log
    if severity != "none":
        anomaly = AnomalyLog(
            battery_id=battery.id,
            timestamp=datetime.utcnow(),
            severity=severity,
            anomaly_type=anomaly_type,
            description=description,
            confidence=confidence,
        )
        db.add(anomaly)
        db.commit()
        db.refresh(anomaly)

        return AnomalyResponse(
            severity=severity,
            anomaly_type=anomaly_type,
            description=description,
            confidence=confidence,
            timestamp=anomaly.timestamp,
        )

    return {"status": "normal", "severity": "none"}

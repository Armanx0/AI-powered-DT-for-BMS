"""Digital Twin routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from app.database import get_db
from app.models.db import Battery, DigitalTwinState
from app.models.schemas import DigitalTwinState as DigitalTwinStateSchema
from app.services.twin_service import TwinService

router = APIRouter()
twin_service = TwinService()


@router.get("/{battery_id}/digital-twin")
async def get_digital_twin(
    battery_id: str,
    db: Session = Depends(get_db)
):
    """Get current digital twin state"""
    battery = db.query(Battery).filter(Battery.battery_id == battery_id).first()
    if not battery:
        raise Exception(f"Battery {battery_id} not found")

    # Get latest twin state
    twin_state = db.query(DigitalTwinState).filter(
        DigitalTwinState.battery_id == battery.id
    ).order_by(desc(DigitalTwinState.timestamp)).first()

    if not twin_state:
        return {"message": "No digital twin state found"}

    return {
        "battery_id": battery.battery_id,
        "soc": twin_state.soc,
        "soh": twin_state.soh,
        "internal_resistance": twin_state.internal_resistance,
        "timestamp": twin_state.timestamp,
        "state_vector": twin_state.state_vector,
    }


@router.get("/{battery_id}/history")
async def get_battery_history(
    battery_id: str,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get battery history"""
    battery = db.query(Battery).filter(Battery.battery_id == battery_id).first()
    if not battery:
        raise Exception(f"Battery {battery_id} not found")

    # Get history
    history = db.query(DigitalTwinState).filter(
        DigitalTwinState.battery_id == battery.id
    ).order_by(desc(DigitalTwinState.timestamp)).limit(limit).all()

    return {
        "battery_id": battery.battery_id,
        "history_count": len(history),
        "history": [
            {
                "timestamp": state.timestamp,
                "soc": state.soc,
                "soh": state.soh,
                "internal_resistance": state.internal_resistance,
            }
            for state in history
        ]
    }

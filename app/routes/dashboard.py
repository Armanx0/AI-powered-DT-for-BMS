"""Dashboard and fleet overview routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import get_db
from app.models.db import Battery, SOCPrediction, SOHPrediction, AnomalyLog

router = APIRouter()


@router.get("/overview")
async def get_fleet_overview(db: Session = Depends(get_db)):
    """Get fleet overview dashboard"""
    # Get all batteries
    batteries = db.query(Battery).all()

    if not batteries:
        return {
            "total_batteries": 0,
            "healthy_batteries": 0,
            "warning_batteries": 0,
            "critical_batteries": 0,
            "average_soc": 0,
            "average_soh": 0,
            "batteries": [],
        }

    # Get latest predictions for each battery
    battery_data = []
    total_soc = 0
    total_soh = 0
    healthy_count = 0
    warning_count = 0
    critical_count = 0

    for battery in batteries:
        # Get latest SOC
        latest_soc = db.query(SOCPrediction).filter(
            SOCPrediction.battery_id == battery.id
        ).order_by(desc(SOCPrediction.timestamp)).first()
        soc = latest_soc.soc if latest_soc else 50

        # Get latest SOH
        latest_soh = db.query(SOHPrediction).filter(
            SOHPrediction.battery_id == battery.id
        ).order_by(desc(SOHPrediction.timestamp)).first()
        soh = latest_soh.soh if latest_soh else 100

        # Count anomalies
        anomalies = db.query(AnomalyLog).filter(
            AnomalyLog.battery_id == battery.id,
            AnomalyLog.is_acknowledged == False
        ).count()

        # Determine status
        if soh < 0.8 or anomalies > 0:
            status = "warning"
            warning_count += 1
        elif soh < 0.5:
            status = "critical"
            critical_count += 1
        else:
            status = "healthy"
            healthy_count += 1

        total_soc += soc
        total_soh += soh

        battery_data.append({
            "battery_id": battery.battery_id,
            "soc": soc,
            "soh": soh,
            "status": status,
            "anomalies": anomalies,
        })

    return {
        "total_batteries": len(batteries),
        "healthy_batteries": healthy_count,
        "warning_batteries": warning_count,
        "critical_batteries": critical_count,
        "average_soc": total_soc / len(batteries),
        "average_soh": total_soh / len(batteries),
        "batteries": battery_data,
    }


@router.get("/alerts")
async def get_fleet_alerts(db: Session = Depends(get_db)):
    """Get active alerts and anomalies"""
    # Get unacknowledged anomalies
    anomalies = db.query(AnomalyLog).filter(
        AnomalyLog.is_acknowledged == False
    ).order_by(desc(AnomalyLog.timestamp)).limit(100).all()

    return {
        "total_alerts": len(anomalies),
        "alerts": [
            {
                "id": anomaly.id,
                "battery_id": anomaly.battery.battery_id if anomaly.battery else None,
                "severity": anomaly.severity,
                "type": anomaly.anomaly_type,
                "description": anomaly.description,
                "timestamp": anomaly.timestamp,
            }
            for anomaly in anomalies
        ]
    }

"""Data upload routes"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import csv
import json
from io import StringIO
from datetime import datetime

from app.database import get_db
from app.models.db import Battery, RawCycle
from app.models.schemas import RawCycleBatch

router = APIRouter()


@router.post("/battery-data")
async def upload_battery_data(
    battery_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload raw battery cycle data (CSV or JSON)"""
    try:
        # Get battery
        battery = db.query(Battery).filter(Battery.battery_id == battery_id).first()
        if not battery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Battery {battery_id} not found"
            )

        # Read and parse file
        contents = await file.read()
        text_data = contents.decode('utf-8')

        if file.filename.endswith('.csv'):
            # Parse CSV
            reader = csv.DictReader(StringIO(text_data))
            count = 0
            for row in reader:
                cycle = RawCycle(
                    battery_id=battery.id,
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    voltage=float(row['voltage']),
                    current=float(row['current']),
                    temperature=float(row['temperature']),
                    capacity=float(row.get('capacity', 0)) or None,
                    internal_resistance=float(row.get('internal_resistance', 0)) or None,
                    re=float(row.get('re', 0)) or None,
                    rct=float(row.get('rct', 0)) or None,
                )
                db.add(cycle)
                count += 1

        elif file.filename.endswith('.json'):
            # Parse JSON
            data = json.loads(text_data)
            count = 0
            for cycle_data in data if isinstance(data, list) else [data]:
                cycle = RawCycle(
                    battery_id=battery.id,
                    timestamp=datetime.fromisoformat(cycle_data['timestamp']),
                    voltage=cycle_data['voltage'],
                    current=cycle_data['current'],
                    temperature=cycle_data['temperature'],
                    capacity=cycle_data.get('capacity'),
                    internal_resistance=cycle_data.get('internal_resistance'),
                    re=cycle_data.get('re'),
                    rct=cycle_data.get('rct'),
                )
                db.add(cycle)
                count += 1

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Use CSV or JSON"
            )

        db.commit()
        return {"message": f"Successfully uploaded {count} cycles", "count": count}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

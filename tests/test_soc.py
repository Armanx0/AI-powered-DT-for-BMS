"""Tests for SOC prediction endpoint"""

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.db import Battery, User
from sqlalchemy.orm import Session

client = TestClient(app)


def test_predict_soc(db: Session):
    """Test SOC prediction endpoint"""
    # Create user and battery
    user = User(username="test", email="test@test.com", hashed_password="hashed")
    db.add(user)
    db.commit()

    battery = Battery(
        battery_id="TEST_BATT_001",
        user_id=user.id,
        battery_type="LiPo",
        nominal_voltage=12.0,
        nominal_capacity=100.0,
        max_charge_current=50.0,
        max_discharge_current=100.0
    )
    db.add(battery)
    db.commit()

    # Test prediction
    response = client.post(
        "/predict/soc",
        params={
            "battery_id": "TEST_BATT_001",
            "voltage": 3.8,
            "current": 25.0,
            "temperature": 25.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "soc" in data
    assert 0 <= data["soc"] <= 100

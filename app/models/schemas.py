"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any


# ============================================
# User Schemas
# ============================================
class UserCreate(BaseModel):
    """User creation request"""
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)


class UserLogin(BaseModel):
    """User login request"""
    username: str
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ============================================
# Battery Schemas
# ============================================
class BatteryCreate(BaseModel):
    """Battery creation request"""
    battery_id: str
    battery_type: str  # "LiPo", "NCA", etc.
    nominal_voltage: float
    nominal_capacity: float
    max_charge_current: float
    max_discharge_current: float
    metadata: Optional[Dict[str, Any]] = None


class Battery(BatteryCreate):
    """Battery response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Cycle Data Schemas
# ============================================
class RawCycleData(BaseModel):
    """Raw cycle data point"""
    timestamp: datetime
    voltage: float
    current: float
    temperature: float
    capacity: Optional[float] = None
    internal_resistance: Optional[float] = None
    re: Optional[float] = None
    rct: Optional[float] = None


class RawCycleBatch(BaseModel):
    """Batch of raw cycle data"""
    battery_id: str
    cycles: List[RawCycleData]


# ============================================
# Prediction Schemas
# ============================================
class SOCPredictionResponse(BaseModel):
    """SOC prediction response"""
    soc: float = Field(..., ge=0, le=100, description="State of Charge (0-100%)")
    confidence: Optional[float] = Field(None, ge=0, le=1)
    timestamp: datetime
    model_version: Optional[str] = None

    class Config:
        from_attributes = True


class SOHPredictionResponse(BaseModel):
    """SOH prediction response"""
    soh: float = Field(..., ge=0, le=100, description="State of Health (0-100%)")
    degradation_rate: Optional[float] = None
    timestamp: datetime
    model_version: Optional[str] = None

    class Config:
        from_attributes = True


class ForecastResponse(BaseModel):
    """Forecast prediction response"""
    future_soc: Optional[List[float]] = None
    future_soh: Optional[List[float]] = None
    future_resistance: Optional[List[float]] = None
    confidence: Optional[float] = Field(None, ge=0, le=1)
    horizon_hours: int
    timestamp: datetime


# ============================================
# Digital Twin Schemas
# ============================================
class DigitalTwinState(BaseModel):
    """Digital Twin state"""
    soc: float
    soh: float
    internal_resistance: Optional[float] = None
    state_vector: Optional[Dict[str, Any]] = None
    timestamp: datetime

    class Config:
        from_attributes = True


# ============================================
# Anomaly Detection Schemas
# ============================================
class AnomalyResponse(BaseModel):
    """Anomaly detection response"""
    severity: str = Field(..., description="low, moderate, high, critical")
    anomaly_type: str
    description: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0, le=1)
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# ============================================
# Health Report Schemas
# ============================================
class BatteryHealthReport(BaseModel):
    """Complete battery health report"""
    battery_id: str
    current_soc: float
    current_soh: float
    current_status: str  # charging, discharging, idle
    internal_resistance: Optional[float] = None
    temperature: Optional[float] = None
    voltage: Optional[float] = None
    last_update: datetime
    recent_anomalies: List[AnomalyResponse] = []
    upcoming_maintenance: Optional[str] = None


# ============================================
# Dashboard Schemas
# ============================================
class BatteryOverview(BaseModel):
    """Fleet battery overview"""
    battery_id: str
    soc: float
    soh: float
    status: str
    last_update: datetime


class FleetOverview(BaseModel):
    """Fleet dashboard overview"""
    total_batteries: int
    healthy_batteries: int
    warning_batteries: int
    critical_batteries: int
    average_soc: float
    average_soh: float
    batteries: List[BatteryOverview]

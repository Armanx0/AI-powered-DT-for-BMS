"""SQLAlchemy ORM models for database tables"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    batteries = relationship("Battery", back_populates="owner")


class Battery(Base):
    """Battery metadata and identification"""
    __tablename__ = "batteries"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    battery_type = Column(String(100), nullable=False)  # "LiPo", "NCA", etc.
    nominal_voltage = Column(Float, nullable=False)
    nominal_capacity = Column(Float, nullable=False)  # Ah
    max_charge_current = Column(Float, nullable=False)
    max_discharge_current = Column(Float, nullable=False)
    metadata = Column(JSON, nullable=True)  # Custom metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="batteries")
    cycles = relationship("RawCycle", back_populates="battery")
    soc_predictions = relationship("SOCPrediction", back_populates="battery")
    soh_predictions = relationship("SOHPrediction", back_populates="battery")
    digital_twin_states = relationship("DigitalTwinState", back_populates="battery")
    forecasts = relationship("Forecast", back_populates="battery")
    anomalies = relationship("AnomalyLog", back_populates="battery")


class RawCycle(Base):
    """Raw telemetry cycles"""
    __tablename__ = "raw_cycles"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    voltage = Column(Float, nullable=False)  # Volts
    current = Column(Float, nullable=False)  # Amps
    temperature = Column(Float, nullable=False)  # Celsius
    capacity = Column(Float, nullable=True)  # Ah
    internal_resistance = Column(Float, nullable=True)  # Ohms
    re = Column(Float, nullable=True)  # Ohms
    rct = Column(Float, nullable=True)  # Ohms
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    battery = relationship("Battery", back_populates="cycles")


class EngineeredFeature(Base):
    """Processed feature vectors"""
    __tablename__ = "engineered_features"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    dv_dt = Column(Float, nullable=True)  # dV/dt
    di_dt = Column(Float, nullable=True)  # dI/dt
    dt_dt = Column(Float, nullable=True)  # dT/dt
    power = Column(Float, nullable=True)  # Watts
    energy = Column(Float, nullable=True)  # Wh
    capacity_fraction = Column(Float, nullable=True)  # %
    resistance_growth = Column(Float, nullable=True)  # %
    features_json = Column(JSON, nullable=True)  # All features in JSON
    created_at = Column(DateTime, default=datetime.utcnow)


class SOCPrediction(Base):
    """State of Charge predictions"""
    __tablename__ = "soc_predictions"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    soc = Column(Float, nullable=False)  # 0-1 or 0-100%
    confidence = Column(Float, nullable=True)  # 0-1
    model_version = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    battery = relationship("Battery", back_populates="soc_predictions")


class SOHPrediction(Base):
    """State of Health predictions"""
    __tablename__ = "soh_predictions"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    soh = Column(Float, nullable=False)  # 0-1 or 0-100%
    degradation_rate = Column(Float, nullable=True)  # % per cycle
    model_version = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    battery = relationship("Battery", back_populates="soh_predictions")


class DigitalTwinState(Base):
    """Digital Twin state snapshots"""
    __tablename__ = "digital_twin_states"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    soc = Column(Float, nullable=False)
    soh = Column(Float, nullable=False)
    internal_resistance = Column(Float, nullable=True)
    state_vector = Column(JSON, nullable=True)  # Complete state representation
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    battery = relationship("Battery", back_populates="digital_twin_states")


class Forecast(Base):
    """Forecast predictions"""
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    forecast_horizon_hours = Column(Integer, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    future_soc = Column(JSON, nullable=True)  # Array of predicted SOC values
    future_soh = Column(JSON, nullable=True)  # Array of predicted SOH values
    future_resistance = Column(JSON, nullable=True)  # Array of predicted resistance values
    confidence = Column(Float, nullable=True)
    model_version = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    battery = relationship("Battery", back_populates="forecasts")


class AnomalyLog(Base):
    """Anomaly detection results"""
    __tablename__ = "anomaly_logs"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    severity = Column(String(50), nullable=False)  # low, moderate, high, critical
    anomaly_type = Column(String(100), nullable=False)  # e.g., "soh_degradation"
    description = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional anomaly details
    is_acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    battery = relationship("Battery", back_populates="anomalies")


class MaintenanceAction(Base):
    """Maintenance recommendations"""
    __tablename__ = "maintenance_actions"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    recommendation = Column(String(500), nullable=False)
    priority = Column(String(50), nullable=False)  # low, medium, high
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

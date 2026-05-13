"""Application constants"""

# ============================================
# Battery States
# ============================================
BATTERY_STATE_CHARGING = "charging"
BATTERY_STATE_DISCHARGING = "discharging"
BATTERY_STATE_IDLE = "idle"

# ============================================
# Anomaly Severity Levels
# ============================================
ANOMALY_SEVERITY_LOW = "low"
ANOMALY_SEVERITY_MODERATE = "moderate"
ANOMALY_SEVERITY_HIGH = "high"
ANOMALY_SEVERITY_CRITICAL = "critical"

ANOMALY_SEVERITIES = [
    ANOMALY_SEVERITY_LOW,
    ANOMALY_SEVERITY_MODERATE,
    ANOMALY_SEVERITY_HIGH,
    ANOMALY_SEVERITY_CRITICAL,
]

# ============================================
# Risk Classes
# ============================================
RISK_CLASS_LOW = "low"
RISK_CLASS_MODERATE = "moderate"
RISK_CLASS_HIGH = "high"
RISK_CLASS_CRITICAL = "critical"

# ============================================
# Feature Engineering Constants
# ============================================
VOLTAGE_MIN = 2.5  # Volts
VOLTAGE_MAX = 4.2  # Volts
TEMPERATURE_MIN = -20  # Celsius
TEMPERATURE_MAX = 60  # Celsius
CURRENT_MAX = 100  # Amps

# ============================================
# Model Performance Targets
# ============================================
SOC_PREDICTION_TOLERANCE = 0.05  # 5%
SOH_PREDICTION_TOLERANCE = 0.10  # 10%

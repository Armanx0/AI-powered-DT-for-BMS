"""Anomaly Detection Service"""

import numpy as np
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class AnomalyService:
    """Hybrid anomaly detection service"""

    def __init__(self):
        """Initialize Anomaly service"""
        pass

    def detect(self, soc: float, soh: float, temperature: float, internal_resistance: float = None):
        """Detect anomalies using hybrid rule-based approach"""
        severity = "none"
        anomaly_type = ""
        description = ""
        confidence = 0.0

        # Rule 1: SOH degradation
        if soh < 0.8:
            severity = "high" if soh < 0.5 else "moderate"
            anomaly_type = "soh_degradation"
            description = f"SOH level {soh*100:.1f}% - Battery nearing end of life"
            confidence = min(0.95, (0.8 - soh) / 0.3)  # Confidence increases as SOH drops

        # Rule 2: Extreme temperature
        elif temperature > settings.ANOMALY_TEMPERATURE_RANGE or temperature < -20:
            severity = "moderate"
            anomaly_type = "temperature_anomaly"
            description = f"Extreme temperature detected: {temperature}°C"
            confidence = 0.85

        # Rule 3: Unusual SOC depletion
        elif soc < 0.05:
            severity = "low"
            anomaly_type = "low_soc"
            description = f"Battery SOC critically low: {soc*100:.1f}%"
            confidence = 0.9

        # Rule 4: Internal resistance increase
        if internal_resistance and internal_resistance > settings.ANOMALY_RESISTANCE_THRESHOLD:
            severity = "high"
            anomaly_type = "resistance_increase"
            description = f"Internal resistance spike: {internal_resistance} Ohms"
            confidence = 0.88

        return severity, anomaly_type, description, confidence

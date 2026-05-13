"""State of Charge (SOC) Service"""

import numpy as np
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class SOCService:
    """Service for SOC predictions"""

    def __init__(self):
        """Initialize SOC service"""
        self.model = None
        if not settings.ENABLE_MOCK_MODELS:
            self._load_model()

    def _load_model(self):
        """Load trained XGBoost SOC model"""
        try:
            import joblib
            import os
            model_path = os.path.join(settings.MODELS_PATH, settings.SOC_MODEL_NAME)
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info(f"Loaded SOC model from {model_path}")
            else:
                logger.warning(f"SOC model not found at {model_path}. Using mock predictions.")
                self.model = None
        except Exception as e:
            logger.error(f"Failed to load SOC model: {e}. Using mock predictions.")
            self.model = None

    def predict(self, voltage: float, current: float, temperature: float) -> float:
        """Predict SOC (0-1)"""
        if self.model is not None:
            try:
                # Prepare features
                features = np.array([[voltage, current, temperature]])
                # Predict
                soc = self.model.predict(features)[0]
                # Ensure bounds
                return float(np.clip(soc, 0, 1))
            except Exception as e:
                logger.error(f"SOC prediction error: {e}")
                return self._mock_predict(voltage, current, temperature)
        else:
            return self._mock_predict(voltage, current, temperature)

    def _mock_predict(self, voltage: float, current: float, temperature: float) -> float:
        """Mock SOC prediction for testing"""
        # Simple mock: normalize voltage to 0-1
        soc = (voltage - 2.5) / (4.2 - 2.5)
        return float(np.clip(soc, 0, 1))

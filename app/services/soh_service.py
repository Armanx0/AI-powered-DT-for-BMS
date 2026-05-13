"""State of Health (SOH) Service"""

import numpy as np
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class SOHService:
    """Service for SOH predictions"""

    def __init__(self):
        """Initialize SOH service"""
        self.model = None
        if not settings.ENABLE_MOCK_MODELS:
            self._load_model()

    def _load_model(self):
        """Load trained XGBoost SOH model"""
        try:
            import joblib
            import os
            model_path = os.path.join(settings.MODELS_PATH, settings.SOH_MODEL_NAME)
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info(f"Loaded SOH model from {model_path}")
            else:
                logger.warning(f"SOH model not found at {model_path}. Using mock predictions.")
                self.model = None
        except Exception as e:
            logger.error(f"Failed to load SOH model: {e}. Using mock predictions.")
            self.model = None

    def predict(self, cycle_count: int, internal_resistance: float) -> float:
        """Predict SOH (0-1)"""
        if self.model is not None:
            try:
                # Prepare features
                features = np.array([[cycle_count, internal_resistance]])
                # Predict
                soh = self.model.predict(features)[0]
                # Ensure bounds
                return float(np.clip(soh, 0, 1))
            except Exception as e:
                logger.error(f"SOH prediction error: {e}")
                return self._mock_predict(cycle_count, internal_resistance)
        else:
            return self._mock_predict(cycle_count, internal_resistance)

    def _mock_predict(self, cycle_count: int, internal_resistance: float) -> float:
        """Mock SOH prediction for testing"""
        # Simple mock: degradation model
        degradation = 0.0005 * cycle_count  # 0.05% per cycle
        soh = 1.0 - degradation
        return float(np.clip(soh, 0, 1))

"""Forecasting Service"""

import numpy as np
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class ForecastService:
    """Service for multi-horizon forecasting"""

    def __init__(self):
        """Initialize Forecast service"""
        self.model = None
        if not settings.ENABLE_MOCK_MODELS:
            self._load_model()

    def _load_model(self):
        """Load trained XGBoost forecast model"""
        try:
            import joblib
            import os
            model_path = os.path.join(settings.MODELS_PATH, settings.FORECAST_MODEL_NAME)
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info(f"Loaded Forecast model from {model_path}")
            else:
                logger.warning(f"Forecast model not found at {model_path}. Using mock predictions.")
                self.model = None
        except Exception as e:
            logger.error(f"Failed to load Forecast model: {e}. Using mock predictions.")
            self.model = None

    def forecast(self, current_soc: float, current_soh: float, horizon_hours: int = 24):
        """Generate multi-horizon forecast"""
        steps = horizon_hours // settings.FORECAST_STEP_SIZE

        if self.model is not None:
            try:
                # Prepare features (simplified)
                features = np.array([[current_soc, current_soh, horizon_hours]])
                # Predict
                future_soc = self.model.predict(features)[0]
                future_soh = self.model.predict(features)[0]
                future_resistance = self.model.predict(features)[0]
                return future_soc, future_soh, future_resistance
            except Exception as e:
                logger.error(f"Forecast error: {e}")
                return self._mock_forecast(current_soc, current_soh, steps)
        else:
            return self._mock_forecast(current_soc, current_soh, steps)

    def _mock_forecast(self, current_soc: float, current_soh: float, steps: int):
        """Mock forecast for testing"""
        # Simple linear degradation
        future_soc = np.linspace(current_soc, max(0, current_soc - 0.05 * steps), steps)
        future_soh = np.linspace(current_soh, max(0, current_soh - 0.01 * steps), steps)
        future_resistance = np.linspace(0.05, 0.05 + 0.001 * steps, steps)

        return future_soc, future_soh, future_resistance

"""
Infrastructure ML: Model Trainer.

Orchestrates training of the anomaly detection ML pipeline.
"""

import os
from typing import List, Dict, Any

from app.infrastructure.ml.models.isolation_forest import IsolationForestDetector
from app.infrastructure.ml.preprocessing.data_preprocessor import DataPreprocessor
from app.config import settings


class AnomalyModelTrainer:
    """Trains and persists anomaly detection models."""

    def __init__(self):
        self._preprocessor = DataPreprocessor()
        self._detector = IsolationForestDetector()

    def train(self, records: List[Dict[str, Any]], model_name: str = "default") -> str:
        """
        Train the anomaly detection model on historical data.

        Args:
            records: Historical supplier transaction data.
            model_name: Name for the saved model file.

        Returns:
            Path to the saved model file.
        """
        # Preprocess
        features = self._preprocessor.transform(records)
        features = self._preprocessor.normalize(features)

        # Train
        self._detector.fit(features)

        # Save
        model_path = os.path.join(settings.MODEL_ARTIFACTS_PATH, f"{model_name}.joblib")
        self._detector.save(model_path)

        return model_path

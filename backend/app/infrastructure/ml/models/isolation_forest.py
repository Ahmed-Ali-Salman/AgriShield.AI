"""
Infrastructure ML: Isolation Forest Anomaly Detector.

Wraps scikit-learn's Isolation Forest for detecting anomalies
in supplier data. This is the ML-based complement to the
rule-based domain service.
"""

from typing import List, Dict, Any

import numpy as np
from sklearn.ensemble import IsolationForest

import joblib
import os


class IsolationForestDetector:
    """
    ML-based anomaly detection using Isolation Forest.

    Used for detecting patterns that rule-based systems cannot catch,
    such as subtle behavioral shifts across multiple dimensions.
    """

    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        self._model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100,
        )
        self._is_fitted = False

    def fit(self, data: np.ndarray) -> None:
        """Train the model on historical supplier data."""
        self._model.fit(data)
        self._is_fitted = True

    def predict(self, data: np.ndarray) -> np.ndarray:
        """
        Predict anomalies.

        Returns:
            Array of -1 (anomaly) or 1 (normal) for each sample.
        """
        if not self._is_fitted:
            raise RuntimeError("Model has not been fitted. Call fit() first.")
        return self._model.predict(data)

    def score_samples(self, data: np.ndarray) -> np.ndarray:
        """Return anomaly scores (lower = more anomalous)."""
        if not self._is_fitted:
            raise RuntimeError("Model has not been fitted. Call fit() first.")
        return self._model.score_samples(data)

    def save(self, path: str) -> None:
        """Persist the trained model to disk."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self._model, path)

    def load(self, path: str) -> None:
        """Load a previously trained model."""
        self._model = joblib.load(path)
        self._is_fitted = True

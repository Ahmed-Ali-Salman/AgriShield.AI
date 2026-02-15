"""
Infrastructure ML: Data Preprocessor.

Transforms raw supplier data into ML-ready feature arrays.
"""

from typing import List, Dict, Any

import numpy as np
import pandas as pd


class DataPreprocessor:
    """Preprocesses raw supplier data for ML models."""

    # Features used for anomaly detection
    NUMERIC_FEATURES = [
        "invoice_total",
        "quantity",
        "unit_price",
        "delivery_days",
        "order_frequency",
    ]

    def transform(self, records: List[Dict[str, Any]]) -> np.ndarray:
        """
        Transform raw records into a numeric feature matrix.

        Args:
            records: List of dictionaries with supplier transaction data.

        Returns:
            2D numpy array suitable for ML model input.
        """
        df = pd.DataFrame(records)

        # Select only numeric features that exist in the data
        available = [f for f in self.NUMERIC_FEATURES if f in df.columns]
        if not available:
            raise ValueError(
                f"No recognized features found. Expected at least one of: {self.NUMERIC_FEATURES}"
            )

        # Fill missing values with column medians
        feature_df = df[available].fillna(df[available].median())

        return feature_df.values

    def normalize(self, data: np.ndarray) -> np.ndarray:
        """Min-max normalize the feature matrix to [0, 1]."""
        mins = data.min(axis=0)
        maxs = data.max(axis=0)
        ranges = maxs - mins
        ranges[ranges == 0] = 1  # Prevent division by zero
        return (data - mins) / ranges

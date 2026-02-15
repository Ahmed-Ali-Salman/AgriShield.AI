"""
Domain Value Object: RiskLevel.

Enumeration of risk classification levels derived from the overall score.
"""

from enum import Enum


class RiskLevel(str, Enum):
    """Risk classification for a supplier's Cyber-Food Risk Score."""

    LOW = "low"          # 0–24:  Minimal risk
    MEDIUM = "medium"    # 25–49: Moderate risk, monitor
    HIGH = "high"        # 50–74: Significant risk, action needed
    CRITICAL = "critical"  # 75–100: Severe risk, immediate action

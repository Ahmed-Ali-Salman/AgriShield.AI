"""Pydantic Schemas: Risk Score."""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class RiskScoreRequest(BaseModel):
    it_security_posture: float = Field(0.0, ge=0, le=100)
    data_consistency: float = Field(0.0, ge=0, le=100)
    delivery_reliability: float = Field(0.0, ge=0, le=100)
    compliance_audit: float = Field(0.0, ge=0, le=100)
    external_risk_factors: float = Field(0.0, ge=0, le=100)

class RiskScoreResponse(BaseModel):
    id: UUID
    supplier_id: UUID
    overall_score: float
    risk_level: str
    computed_at: datetime
    notes: str
    class Config:
        from_attributes = True

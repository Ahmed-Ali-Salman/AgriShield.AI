"""Presentation: Risk Score API Routes."""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from app.presentation.dependencies.container import get_calculate_risk_score_uc, get_risk_history_uc
from app.presentation.dependencies.auth import get_current_user
from app.presentation.schemas.risk_score_schemas import RiskScoreRequest, RiskScoreResponse
from app.application.dto.risk_score_dto import RiskScoreInputDTO

router = APIRouter()

@router.post("/{supplier_id}", response_model=RiskScoreResponse, status_code=201)
async def calculate_risk_score(supplier_id: UUID, body: RiskScoreRequest, use_case=Depends(get_calculate_risk_score_uc), _=Depends(get_current_user)):
    dto = RiskScoreInputDTO(**body.model_dump())
    return await use_case.execute(supplier_id, dto)

@router.get("/{supplier_id}/history", response_model=List[RiskScoreResponse])
async def get_risk_history(supplier_id: UUID, limit: int = 30, use_case=Depends(get_risk_history_uc), _=Depends(get_current_user)):
    return await use_case.execute(supplier_id, limit=limit)

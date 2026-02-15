"""Presentation: Alert API Routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.presentation.dependencies.container import get_create_alert_uc, get_list_alerts_uc
from app.presentation.dependencies.auth import get_current_user
from app.presentation.schemas.alert_schemas import AlertCreateRequest, AlertResponse
from app.application.dto.alert_dto import CreateAlertDTO

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(status: Optional[str] = None, skip: int = 0, limit: int = 50, use_case=Depends(get_list_alerts_uc), _=Depends(get_current_user)):
    return await use_case.execute(status=status, skip=skip, limit=limit)

@router.post("/", response_model=AlertResponse, status_code=201)
async def create_alert(body: AlertCreateRequest, use_case=Depends(get_create_alert_uc), _=Depends(get_current_user)):
    dto = CreateAlertDTO(supplier_id=body.supplier_id, title=body.title, description=body.description, severity=body.severity)
    return await use_case.execute(dto)

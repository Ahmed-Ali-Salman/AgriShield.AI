"""Presentation: Alert API Routes."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from app.presentation.dependencies.container import get_create_alert_uc, get_list_alerts_uc, get_alert_repo
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

class AlertStatusUpdate(BaseModel):
    status: str  # "acknowledged" or "resolved"

@router.patch("/{alert_id}", response_model=AlertResponse)
async def update_alert_status(
    alert_id: UUID,
    body: AlertStatusUpdate,
    alert_repo=Depends(get_alert_repo),
    _=Depends(get_current_user),
):
    alert = await alert_repo.get_by_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    valid_statuses = ["open", "acknowledged", "resolved"]
    if body.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {valid_statuses}")

    from app.domain.entities.alert import AlertStatus
    alert.status = AlertStatus(body.status)
    if body.status == "resolved":
        alert.resolved_at = datetime.utcnow()

    updated = await alert_repo.update(alert)
    return updated

"""Presentation: Anomaly API Routes."""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from app.presentation.dependencies.container import get_anomalies_uc, get_detect_anomalies_uc
from app.presentation.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/supplier/{supplier_id}")
async def get_supplier_anomalies(supplier_id: UUID, use_case=Depends(get_anomalies_uc), _=Depends(get_current_user)):
    return await use_case.get_by_supplier(supplier_id)

@router.get("/unreviewed")
async def get_unreviewed(use_case=Depends(get_anomalies_uc), _=Depends(get_current_user)):
    return await use_case.get_unreviewed()

@router.post("/detect/{supplier_id}")
async def detect_anomalies(supplier_id: UUID, data: dict, use_case=Depends(get_detect_anomalies_uc), _=Depends(get_current_user)):
    count = await use_case.execute(supplier_id, data)
    return {"anomalies_detected": count}

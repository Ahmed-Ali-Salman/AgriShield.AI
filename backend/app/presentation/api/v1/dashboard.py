"""Presentation: Dashboard API Routes."""
from fastapi import APIRouter, Depends
from app.presentation.dependencies.container import get_supplier_repo, get_alert_repo, get_risk_score_repo
from app.presentation.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/summary")
async def dashboard_summary(supplier_repo=Depends(get_supplier_repo), alert_repo=Depends(get_alert_repo), _=Depends(get_current_user)):
    return {
        "total_suppliers": await supplier_repo.count(),
        "open_alerts": await alert_repo.count_open(),
    }

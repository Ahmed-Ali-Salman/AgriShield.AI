"""Presentation: Dashboard API Routes."""
from fastapi import APIRouter, Depends
from app.presentation.dependencies.container import get_supplier_repo, get_alert_repo, get_risk_score_repo
from app.presentation.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/summary")
async def dashboard_summary(
    supplier_repo=Depends(get_supplier_repo),
    alert_repo=Depends(get_alert_repo),
    risk_score_repo=Depends(get_risk_score_repo),
    _=Depends(get_current_user),
):
    total_suppliers = await supplier_repo.count()
    open_alerts = await alert_repo.count_open()

    # Get latest risk scores for all suppliers
    all_suppliers = await supplier_repo.get_all(skip=0, limit=1000)
    scores = []
    high_risk_count = 0
    for s in all_suppliers:
        history = await risk_score_repo.get_history(s.id, limit=1)
        if history:
            latest = history[0]
            scores.append(latest.overall_score)
            if latest.risk_level.value in ("high", "critical"):
                high_risk_count += 1

    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

    return {
        "total_suppliers": total_suppliers,
        "open_alerts": open_alerts,
        "high_risk_count": high_risk_count,
        "avg_risk_score": avg_score,
    }

"""
Presentation: API v1 Router.

Aggregates all v1 route modules into a single router.
"""

from fastapi import APIRouter

from app.presentation.api.v1.suppliers import router as suppliers_router
from app.presentation.api.v1.risk_scores import router as risk_scores_router
from app.presentation.api.v1.alerts import router as alerts_router
from app.presentation.api.v1.anomalies import router as anomalies_router
from app.presentation.api.v1.auth import router as auth_router
from app.presentation.api.v1.dashboard import router as dashboard_router
from app.presentation.api.v1.data_ingestion import router as ingestion_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(suppliers_router, prefix="/suppliers", tags=["Suppliers"])
api_v1_router.include_router(risk_scores_router, prefix="/risk-scores", tags=["Risk Scores"])
api_v1_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
api_v1_router.include_router(anomalies_router, prefix="/anomalies", tags=["Anomalies"])
api_v1_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_v1_router.include_router(ingestion_router, prefix="/data", tags=["Data Ingestion"])

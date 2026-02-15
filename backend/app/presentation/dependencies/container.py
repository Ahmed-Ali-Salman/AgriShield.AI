"""
Presentation: DI Container.

Dependency Injection container that wires together all layers.
This is the ONLY place where concrete infrastructure implementations
are imported — enforcing the Dependency Inversion Principle.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import get_db_session

# --- Repositories (concrete → abstract interface) ---
from app.infrastructure.database.repositories.pg_supplier_repository import PgSupplierRepository
from app.infrastructure.database.repositories.pg_risk_score_repository import PgRiskScoreRepository
from app.infrastructure.database.repositories.pg_alert_repository import PgAlertRepository
from app.infrastructure.database.repositories.pg_user_repository import PgUserRepository
from app.infrastructure.database.repositories.pg_anomaly_repository import PgAnomalyRepository

# --- Domain Services ---
from app.domain.services.risk_scoring_service import RiskScoringService
from app.domain.services.anomaly_detection_service import AnomalyDetectionService

# --- Infrastructure Services ---
from app.infrastructure.security.jwt_handler import JWTAuthService
from app.infrastructure.services.email_notification_service import EmailNotificationService
from app.infrastructure.services.csv_parser_service import CSVParserService

# --- Use Cases ---
from app.application.use_cases.suppliers.create_supplier import CreateSupplierUseCase
from app.application.use_cases.suppliers.get_supplier import GetSupplierUseCase
from app.application.use_cases.suppliers.list_suppliers import ListSuppliersUseCase
from app.application.use_cases.suppliers.update_supplier import UpdateSupplierUseCase
from app.application.use_cases.risk_scoring.calculate_risk_score import CalculateRiskScoreUseCase
from app.application.use_cases.risk_scoring.get_risk_history import GetRiskHistoryUseCase
from app.application.use_cases.anomalies.detect_anomalies import DetectAnomaliesUseCase
from app.application.use_cases.anomalies.get_anomalies import GetAnomaliesUseCase
from app.application.use_cases.alerts.create_alert import CreateAlertUseCase
from app.application.use_cases.alerts.list_alerts import ListAlertsUseCase
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.register import RegisterUseCase
from app.application.use_cases.data_ingestion.upload_csv import UploadCSVUseCase


# ========================================
# Factory functions for FastAPI Depends()
# ========================================

def get_supplier_repo(session: AsyncSession = Depends(get_db_session)):
    return PgSupplierRepository(session)

def get_risk_score_repo(session: AsyncSession = Depends(get_db_session)):
    return PgRiskScoreRepository(session)

def get_alert_repo(session: AsyncSession = Depends(get_db_session)):
    return PgAlertRepository(session)

def get_user_repo(session: AsyncSession = Depends(get_db_session)):
    return PgUserRepository(session)

def get_anomaly_repo(session: AsyncSession = Depends(get_db_session)):
    return PgAnomalyRepository(session)

def get_auth_service():
    return JWTAuthService()

def get_scoring_service():
    return RiskScoringService()

def get_detection_service():
    return AnomalyDetectionService()

def get_notification_service():
    return EmailNotificationService()

def get_file_parser():
    return CSVParserService()


# --- Use Case Factories ---

def get_create_supplier_uc(repo=Depends(get_supplier_repo)):
    return CreateSupplierUseCase(repo)

def get_get_supplier_uc(repo=Depends(get_supplier_repo)):
    return GetSupplierUseCase(repo)

def get_list_suppliers_uc(repo=Depends(get_supplier_repo)):
    return ListSuppliersUseCase(repo)

def get_update_supplier_uc(repo=Depends(get_supplier_repo)):
    return UpdateSupplierUseCase(repo)

def get_calculate_risk_score_uc(
    supplier_repo=Depends(get_supplier_repo),
    risk_repo=Depends(get_risk_score_repo),
    scoring_svc=Depends(get_scoring_service),
):
    return CalculateRiskScoreUseCase(supplier_repo, risk_repo, scoring_svc)

def get_risk_history_uc(repo=Depends(get_risk_score_repo)):
    return GetRiskHistoryUseCase(repo)

def get_detect_anomalies_uc(
    detection_svc=Depends(get_detection_service),
    anomaly_repo=Depends(get_anomaly_repo),
):
    return DetectAnomaliesUseCase(detection_svc, anomaly_repo)

def get_anomalies_uc(repo=Depends(get_anomaly_repo)):
    return GetAnomaliesUseCase(repo)

def get_create_alert_uc(
    repo=Depends(get_alert_repo),
    notifier=Depends(get_notification_service),
):
    return CreateAlertUseCase(repo, notifier)

def get_list_alerts_uc(repo=Depends(get_alert_repo)):
    return ListAlertsUseCase(repo)

def get_login_uc(repo=Depends(get_user_repo), auth=Depends(get_auth_service)):
    return LoginUseCase(repo, auth)

def get_register_uc(repo=Depends(get_user_repo), auth=Depends(get_auth_service)):
    return RegisterUseCase(repo, auth)

def get_upload_csv_uc(parser=Depends(get_file_parser)):
    return UploadCSVUseCase(parser)

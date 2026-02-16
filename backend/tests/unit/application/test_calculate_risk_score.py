"""Unit tests: Calculate Risk Score Use Case (with mocked repo)."""
import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.application.use_cases.risk_scoring.calculate_risk_score import CalculateRiskScoreUseCase
from app.application.dto.risk_score_dto import RiskScoreInputDTO
from app.domain.services.risk_scoring_service import RiskScoringService
from app.domain.entities.supplier import Supplier
from app.domain.value_objects.risk_level import RiskLevel


@pytest.fixture
def supplier():
    return Supplier(
        id=uuid4(),
        name="Test Supplier",
        country="Egypt",
        category="produce",
        contact_email="test@test.com",
    )


@pytest.fixture
def mock_supplier_repo(supplier):
    repo = AsyncMock()
    repo.get_by_id.return_value = supplier
    return repo


@pytest.fixture
def mock_risk_repo():
    repo = AsyncMock()
    repo.create.side_effect = lambda score: score  # Return the score as-is
    return repo


@pytest.fixture
def scoring_service():
    return RiskScoringService()


@pytest.fixture
def use_case(mock_supplier_repo, mock_risk_repo, scoring_service):
    return CalculateRiskScoreUseCase(mock_supplier_repo, mock_risk_repo, scoring_service)


class TestCalculateRiskScoreUseCase:
    @pytest.mark.asyncio
    async def test_computes_and_persists_score(self, use_case, supplier, mock_risk_repo):
        dto = RiskScoreInputDTO(
            it_security_posture=50,
            data_consistency=50,
            delivery_reliability=50,
            compliance_audit=50,
            external_risk_factors=50,
        )

        result = await use_case.execute(supplier.id, dto)

        assert result is not None
        assert result.overall_score == 50.0
        assert result.risk_level == RiskLevel.HIGH
        mock_risk_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_supplier_not_found_raises(self, mock_risk_repo, scoring_service):
        repo = AsyncMock()
        repo.get_by_id.return_value = None
        uc = CalculateRiskScoreUseCase(repo, mock_risk_repo, scoring_service)

        dto = RiskScoreInputDTO(it_security_posture=50)
        with pytest.raises(ValueError, match="not found"):
            await uc.execute(uuid4(), dto)

    @pytest.mark.asyncio
    async def test_low_risk_input(self, use_case, supplier, mock_risk_repo):
        dto = RiskScoreInputDTO(
            it_security_posture=10,
            data_consistency=10,
            delivery_reliability=10,
            compliance_audit=10,
            external_risk_factors=10,
        )

        result = await use_case.execute(supplier.id, dto)
        assert result.overall_score == 10.0
        assert result.risk_level == RiskLevel.LOW

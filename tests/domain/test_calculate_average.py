"""Тесты для CalculateAverageUseCase."""
import pytest
from decimal import Decimal
from domain.use_cases.calculate_average import CalculateAverageUseCase


class TestCalculateAverageUseCase:

    @pytest.fixture
    def use_case(self):
        return CalculateAverageUseCase()

    def test_average_price_calculation(self, use_case, sample_deals):
        result = use_case.execute(sample_deals)
        assert result.total_shares == 30
        assert result.ticker == "SBER"

    def test_empty_deals_raises_error(self, use_case):
        from core.exceptions import CalculationError
        with pytest.raises(CalculationError, match="Нет сделок на покупку"):
            use_case.execute([])

    def test_commission_included(self, use_case, sample_deals):
        result = use_case.execute(sample_deals)
        expected_cost = (
            10 * Decimal("270.50") +
            5 * Decimal("265.00") +
            15 * Decimal("275.00")
        )
        assert result.total_invested > expected_cost

    def test_unrealized_pnl(self, use_case, sample_deals):
        current_price = Decimal("280.00")
        result = use_case.execute(sample_deals, current_price)
        expected_pnl = (current_price - result.average_price) * result.total_shares
        assert result.unrealized_pnl == expected_pnl
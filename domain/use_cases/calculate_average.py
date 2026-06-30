"""Use Case: Расчет средней цены позиции."""

from decimal import Decimal
from typing import List, Optional
from domain.models.deal import Deal, AverageResult
from domain.services.commission_calculator import CommissionCalculator
from core.exceptions import CalculationError


class CalculateAverageUseCase:
    """Расчет средней цены позиции с учетом комиссий."""

    def __init__(self, commission_calculator: Optional[CommissionCalculator] = None):
        self._commission_calc = commission_calculator or CommissionCalculator()

    def execute(
        self,
        deals: List[Deal],
        current_price: Optional[Decimal] = None,
    ) -> AverageResult:
        buy_deals = [d for d in deals if d.is_buy]
        if not buy_deals:
            raise CalculationError("Нет сделок на покупку для расчета средней цены")

        total_shares = sum(d.quantity for d in buy_deals)
        total_cost = sum(d.total_cost for d in buy_deals)
        total_commission = sum(
            d.commission if d.commission > 0
            else self._commission_calc.calculate(d.total_cost)
            for d in buy_deals
        )

        average_price = total_cost / total_shares
        total_invested = total_cost + total_commission

        return AverageResult(
            ticker=buy_deals[0].ticker,
            deals=buy_deals,
            total_shares=total_shares,
            average_price=average_price,
            total_invested=total_invested,
            current_price=current_price,
        )
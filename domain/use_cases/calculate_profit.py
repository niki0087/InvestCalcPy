"""Use Case: Расчет прибыли/убытка от спекулятивной сделки."""

from decimal import Decimal
from domain.models.profit import TradeDeal, ProfitResult
from domain.services.tax_calculator import TaxCalculator


class CalculateProfitUseCase:
    """Расчет чистой прибыли с учетом комиссий и налогов."""

    def __init__(self, tax_calculator: TaxCalculator = None):
        self._tax_calc = tax_calculator or TaxCalculator()

    def execute(self, deal: TradeDeal) -> ProfitResult:
        gross_profit = deal.gross_profit
        tax_amount = self._tax_calc.calculate_tax(gross_profit)
        net_profit = gross_profit - tax_amount

        if deal.buy_cost == 0:
            profit_percent = Decimal('0')
        else:
            profit_percent = (net_profit / deal.buy_cost) * 100

        return ProfitResult(
            deal=deal,
            net_profit=net_profit,
            tax_amount=tax_amount,
            profit_percent=profit_percent,
        )
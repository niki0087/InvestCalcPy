"""Use Case: Расчет дивидендной доходности."""

from decimal import Decimal
from domain.models.dividend import DividendInfo, DividendResult
from domain.services.tax_calculator import TaxCalculator
from core.constants import DEFAULT_KEY_RATE, DEFAULT_TAX_RATE


class CalculateDividendsUseCase:
    """Расчет дивидендной доходности."""

    def __init__(self, tax_calculator: TaxCalculator = None):
        self._tax_calc = tax_calculator or TaxCalculator()

    def execute(
        self,
        ticker: str,
        dividend_per_share: Decimal,
        shares_count: int,
        stock_price: Decimal,
        key_rate: Decimal = DEFAULT_KEY_RATE,
        payments_per_year: int = 1,
    ) -> DividendResult:
        info = DividendInfo(
            ticker=ticker,
            dividend_per_share=dividend_per_share,
            shares_count=shares_count,
            stock_price=stock_price,
            tax_rate=DEFAULT_TAX_RATE,
        )

        annual_yield = info.dividend_yield * payments_per_year
        comparison = annual_yield - key_rate
        monthly_income = info.net_dividend * payments_per_year / 12

        return DividendResult(
            info=info,
            annual_yield=annual_yield,
            monthly_income=monthly_income,
            comparison_with_deposit=comparison,
        )
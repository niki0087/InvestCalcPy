"""Модели для расчета дивидендной доходности."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DividendInfo:
    """Информация о дивидендах."""
    ticker: str
    dividend_per_share: Decimal
    shares_count: int
    stock_price: Decimal
    tax_rate: Decimal = Decimal('0.13')

    @property
    def gross_dividend(self) -> Decimal:
        return self.dividend_per_share * self.shares_count

    @property
    def tax_amount(self) -> Decimal:
        return self.gross_dividend * self.tax_rate

    @property
    def net_dividend(self) -> Decimal:
        return self.gross_dividend - self.tax_amount

    @property
    def dividend_yield(self) -> Decimal:
        if self.stock_price == 0:
            return Decimal('0')
        return (self.dividend_per_share / self.stock_price) * 100


@dataclass(frozen=True)
class DividendResult:
    """Результат расчета дивидендов."""
    info: DividendInfo
    annual_yield: Decimal
    monthly_income: Decimal
    comparison_with_deposit: Decimal
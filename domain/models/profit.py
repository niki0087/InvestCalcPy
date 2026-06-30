"""Модели для расчета прибыли/убытка от торговой операции."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class TradeDeal:
    """Торговая сделка (покупка + продажа)."""
    ticker: str
    buy_price: Decimal
    sell_price: Decimal
    quantity: int
    buy_commission: Decimal = Decimal('0')
    sell_commission: Decimal = Decimal('0')

    @property
    def buy_cost(self) -> Decimal:
        return self.buy_price * self.quantity + self.buy_commission

    @property
    def sell_revenue(self) -> Decimal:
        return self.sell_price * self.quantity - self.sell_commission

    @property
    def gross_profit(self) -> Decimal:
        return self.sell_revenue - self.buy_cost


@dataclass(frozen=True)
class ProfitResult:
    """Результат расчета прибыли."""
    deal: TradeDeal
    net_profit: Decimal
    tax_amount: Decimal
    profit_percent: Decimal
    annualized_return: Optional[Decimal] = None
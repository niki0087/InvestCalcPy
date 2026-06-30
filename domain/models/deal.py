"""Модели для расчета средней цены позиции."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Deal:
    """Сделка покупки/продажи актива."""
    ticker: str
    quantity: int
    price_per_share: Decimal
    commission: Decimal = Decimal('0')
    is_buy: bool = True
    deal_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def total_cost(self) -> Decimal:
        return self.price_per_share * self.quantity

    @property
    def total_with_commission(self) -> Decimal:
        if self.is_buy:
            return self.total_cost + self.commission
        return self.total_cost - self.commission


@dataclass(frozen=True)
class AverageResult:
    """Результат расчета усреднения позиции."""
    ticker: str
    deals: List[Deal]
    total_shares: int
    average_price: Decimal
    total_invested: Decimal
    current_price: Optional[Decimal] = None

    @property
    def unrealized_pnl(self) -> Optional[Decimal]:
        if self.current_price is None:
            return None
        return (self.current_price - self.average_price) * self.total_shares

    @property
    def unrealized_pnl_percent(self) -> Optional[Decimal]:
        if self.current_price is None or self.average_price == 0:
            return None
        return ((self.current_price - self.average_price) / self.average_price) * 100

    @property
    def break_even_price(self) -> Decimal:
        total_commission = sum(d.commission for d in self.deals)
        total_cost = sum(d.total_cost for d in self.deals)
        if self.total_shares == 0:
            return Decimal('0')
        return (total_cost + total_commission) / self.total_shares
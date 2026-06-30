"""Калькулятор комиссий брокера."""

from decimal import Decimal
from typing import List
from domain.models.deal import Deal
from core.constants import DEFAULT_COMMISSION_RATE, MIN_COMMISSION, DEPOSITARY_COMMISSION_RATE


class CommissionCalculator:
    """Рассчитывает комиссии по сделкам."""

    def __init__(
        self,
        broker_rate: Decimal = DEFAULT_COMMISSION_RATE,
        min_commission: Decimal = MIN_COMMISSION,
        depositary_rate: Decimal = DEPOSITARY_COMMISSION_RATE,
    ):
        self._broker_rate = broker_rate
        self._min_commission = min_commission
        self._depositary_rate = depositary_rate

    def calculate(self, amount: Decimal, is_sell: bool = False) -> Decimal:
        commission = amount * self._broker_rate
        if commission < self._min_commission:
            commission = self._min_commission
        if is_sell:
            commission += amount * self._depositary_rate
        return commission

    def calculate_total(self, deals: List[Deal]) -> Decimal:
        return sum(
            d.commission if d.commission > 0
            else self.calculate(d.total_cost, is_sell=not d.is_buy)
            for d in deals
        )
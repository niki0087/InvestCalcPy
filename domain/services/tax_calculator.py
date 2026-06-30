"""Калькулятор налогов."""

from decimal import Decimal
from core.constants import DEFAULT_TAX_RATE


class TaxCalculator:
    """Рассчитывает налог на доходы физических лиц (НДФЛ)."""

    def __init__(self, tax_rate: Decimal = DEFAULT_TAX_RATE):
        self._tax_rate = tax_rate

    def calculate_tax(self, income: Decimal) -> Decimal:
        if income <= 0:
            return Decimal('0')
        return income * self._tax_rate

    def calculate_net_income(self, gross_income: Decimal) -> Decimal:
        tax = self.calculate_tax(gross_income)
        return gross_income - tax
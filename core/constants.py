"""Бизнес-константы приложения."""

from decimal import Decimal

DEFAULT_COMMISSION_RATE = Decimal('0.0005')
MIN_COMMISSION = Decimal('0.01')
DEPOSITARY_COMMISSION_RATE = Decimal('0.0001')
DEFAULT_TAX_RATE = Decimal('0.13')
DEFAULT_KEY_RATE = Decimal('16.0')

CURRENCY_FORMAT = '{:,.2f} ₽'
PERCENT_FORMAT = '{:+.2f}%'
QUANTITY_FORMAT = '{} шт.'
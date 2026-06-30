"""Утилиты форматирования и валидации."""

from decimal import Decimal, InvalidOperation
from typing import Optional


def format_currency(amount: Decimal, with_sign: bool = False) -> str:
    if with_sign:
        sign = '+' if amount >= 0 else ''
        return f"{sign}{amount:,.2f} ₽"
    return f"{amount:,.2f} ₽"


def format_percent(value: Decimal) -> str:
    sign = '+' if value > 0 else ''
    return f"{sign}{value:.2f}%"


def validate_positive_number(value: str) -> Optional[Decimal]:
    try:
        cleaned = value.replace(',', '.').strip()
        if not cleaned:
            return None
        num = Decimal(cleaned)
        if num < 0:
            return None
        return num
    except (InvalidOperation, ValueError):
        return None


def validate_integer(value: str) -> Optional[int]:
    try:
        cleaned = value.strip()
        if not cleaned:
            return None
        num = int(cleaned)
        if num < 0:
            return None
        return num
    except (ValueError, TypeError):
        return None
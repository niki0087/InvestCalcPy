"""Domain models."""
from .deal import Deal, AverageResult
from .dividend import DividendInfo, DividendResult
from .profit import TradeDeal, ProfitResult

__all__ = [
    'Deal', 'AverageResult',
    'DividendInfo', 'DividendResult',
    'TradeDeal', 'ProfitResult',
]
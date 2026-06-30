"""Базовые исключения приложения."""


class InvestCalcException(Exception):
    """Базовое исключение приложения."""
    pass


class ValidationError(InvestCalcException):
    """Ошибка валидации данных."""
    pass


class CalculationError(InvestCalcException):
    """Ошибка в бизнес-расчетах."""
    pass


class RepositoryError(InvestCalcException):
    """Ошибка работы с данными."""
    pass


class APIError(InvestCalcException):
    """Ошибка внешнего API."""
    pass
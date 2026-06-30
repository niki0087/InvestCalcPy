"""Презентер для калькулятора дивидендов."""

from decimal import Decimal
from domain.use_cases.calculate_dividends import CalculateDividendsUseCase
from core.utils import validate_positive_number, validate_integer, format_currency, format_percent


class DividendPresenter:

    def __init__(self, use_case: CalculateDividendsUseCase):
        self._use_case = use_case
        self._view = None

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value

    def calculate(self, ticker: str, price_text: str, quantity_text: str,
                  dividend_text: str, key_rate_text: str):
        errors = []
        if not ticker:
            errors.append("Введите тикер")

        price = validate_positive_number(price_text)
        if price is None or price == 0:
            errors.append("Некорректная цена акции")

        quantity = validate_integer(quantity_text)
        if quantity is None or quantity == 0:
            errors.append("Количество должно быть целым положительным числом")

        dividend = validate_positive_number(dividend_text)
        if dividend is None:
            errors.append("Некорректный дивиденд на акцию")

        key_rate = validate_positive_number(key_rate_text)
        if key_rate is None:
            key_rate = Decimal('16.0')

        if errors:
            if self._view:
                self._view.show_error(". ".join(errors))
            return

        try:
            result = self._use_case.execute(
                ticker=ticker,
                dividend_per_share=dividend,
                shares_count=quantity,
                stock_price=price,
                key_rate=key_rate,
            )

            comparison = result.comparison_with_deposit
            comp_text = f"{'+' if comparison >= 0 else ''}{comparison:.2f} п.п."
            comp_positive = comparison >= 0

            if self._view:
                self._view.show_result([
                    ("Тикер", result.info.ticker, False),
                    ("Дивидендная доходность", format_percent(result.info.dividend_yield), True),
                    ("Годовая ДД", format_percent(result.annual_yield), True),
                    ("Дивиденды до налога", format_currency(result.info.gross_dividend), True),
                    ("Налог (13%)", format_currency(result.info.tax_amount), False),
                    ("Чистый доход", format_currency(result.info.net_dividend), True),
                    ("Доход в месяц", format_currency(result.monthly_income), True),
                    ("Сравнение с депозитом", comp_text, comp_positive),
                ])

                if result.annual_yield > 10:
                    self._view.show_error("Внимание: доходность >10% — высокий риск!")

        except Exception as e:
            if self._view:
                self._view.show_error(str(e))
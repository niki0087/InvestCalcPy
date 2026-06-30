"""Презентер для калькулятора усреднения."""

from decimal import Decimal
from typing import List
from domain.models.deal import Deal
from domain.use_cases.calculate_average import CalculateAverageUseCase
from core.utils import validate_positive_number, validate_integer, format_currency


class AveragePresenter:

    def __init__(self, use_case: CalculateAverageUseCase):
        self._use_case = use_case
        self._deals: List[Deal] = []
        self._view = None

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value

    def add_deal(self, ticker: str, price_text: str, quantity_text: str,
                 commission_text: str):
        errors = []
        if not ticker:
            errors.append("Введите тикер")

        price = validate_positive_number(price_text)
        if price is None:
            errors.append("Некорректная цена")

        quantity = validate_integer(quantity_text)
        if quantity is None:
            errors.append("Количество должно быть целым положительным числом")

        commission = validate_positive_number(commission_text)
        if commission is None:
            commission = Decimal('0')

        if errors:
            if self._view:
                self._view.show_error(". ".join(errors))
            return

        deal = Deal(
            ticker=ticker,
            quantity=quantity,
            price_per_share=price,
            commission=commission,
        )
        self._deals.append(deal)

        if self._view:
            self._view.update_deals_list(self._format_deals())
            self._view.clear_inputs()

    def remove_deal(self, index: int):
        if 0 <= index < len(self._deals):
            self._deals.pop(index)
            if self._view:
                self._view.update_deals_list(self._format_deals())

    def calculate(self):
        if not self._deals:
            if self._view:
                self._view.show_error("Добавьте хотя бы одну сделку")
            return

        try:
            result = self._use_case.execute(self._deals)
            if self._view:
                self._view.show_result({
                    "Тикер": result.ticker,
                    "Всего акций": f"{result.total_shares} шт.",
                    "Средняя цена": format_currency(result.average_price),
                    "Всего инвестировано": format_currency(result.total_invested),
                    "Цена безубыточности": format_currency(result.break_even_price),
                })
        except Exception as e:
            if self._view:
                self._view.show_error(str(e))

    def _format_deals(self) -> list:
        return [
            {
                "ticker": d.ticker,
                "quantity": d.quantity,
                "price": format_currency(d.price_per_share),
                "commission": format_currency(d.commission),
            }
            for d in self._deals
        ]
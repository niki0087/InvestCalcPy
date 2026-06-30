"""Фикстуры для тестов pytest."""
import pytest
from decimal import Decimal
from domain.models.deal import Deal
from domain.models.dividend import DividendInfo
from domain.models.profit import TradeDeal


@pytest.fixture
def sample_deals():
    return [
        Deal(ticker="SBER", quantity=10, price_per_share=Decimal("270.50"), commission=Decimal("1.35")),
        Deal(ticker="SBER", quantity=5, price_per_share=Decimal("265.00"), commission=Decimal("0.66")),
        Deal(ticker="SBER", quantity=15, price_per_share=Decimal("275.00"), commission=Decimal("2.06")),
    ]


@pytest.fixture
def sample_dividend_info():
    return DividendInfo(
        ticker="SBER",
        dividend_per_share=Decimal("33.30"),
        shares_count=100,
        stock_price=Decimal("270.50"),
    )


@pytest.fixture
def sample_trade_deal():
    return TradeDeal(
        ticker="SBER",
        buy_price=Decimal("270.00"),
        sell_price=Decimal("285.00"),
        quantity=10,
        buy_commission=Decimal("1.35"),
        sell_commission=Decimal("1.43"),
    )
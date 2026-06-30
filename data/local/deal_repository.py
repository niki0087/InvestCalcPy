"""Реализация репозитория сделок на SQLite."""

from typing import List
from uuid import UUID
from sqlalchemy import select, delete
from data.local.database import async_session
from data.local.models import DealModel
from domain.interfaces.repository import DealRepository
from domain.models.deal import Deal


class SQLiteDealRepository(DealRepository):

    async def save(self, deal: Deal) -> None:
        async with async_session() as session:
            model = DealModel(
                deal_id=deal.deal_id,
                ticker=deal.ticker,
                quantity=deal.quantity,
                price_per_share=deal.price_per_share,
                commission=deal.commission,
                is_buy=deal.is_buy,
                timestamp=deal.timestamp,
            )
            session.add(model)
            await session.commit()

    async def get_by_ticker(self, ticker: str) -> List[Deal]:
        async with async_session() as session:
            result = await session.execute(
                select(DealModel).where(DealModel.ticker == ticker)
            )
            models = result.scalars().all()
            return [self._to_domain(m) for m in models]

    async def get_all(self) -> List[Deal]:
        async with async_session() as session:
            result = await session.execute(select(DealModel))
            models = result.scalars().all()
            return [self._to_domain(m) for m in models]

    async def delete(self, deal_id: UUID) -> None:
        async with async_session() as session:
            await session.execute(
                delete(DealModel).where(DealModel.deal_id == deal_id)
            )
            await session.commit()

    async def delete_all(self) -> None:
        async with async_session() as session:
            await session.execute(delete(DealModel))
            await session.commit()

    def _to_domain(self, model: DealModel) -> Deal:
        return Deal(
            deal_id=model.deal_id,
            ticker=model.ticker,
            quantity=model.quantity,
            price_per_share=model.price_per_share,
            commission=model.commission,
            is_buy=model.is_buy,
            timestamp=model.timestamp,
        )
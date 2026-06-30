"""Абстрактный интерфейс репозитория сделок."""

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID


class DealRepository(ABC):
    """Абстрактный репозиторий для работы со сделками."""

    @abstractmethod
    async def save(self, deal) -> None:
        ...

    @abstractmethod
    async def get_by_ticker(self, ticker: str) -> List:
        ...

    @abstractmethod
    async def get_all(self) -> List:
        ...

    @abstractmethod
    async def delete(self, deal_id: UUID) -> None:
        ...

    @abstractmethod
    async def delete_all(self) -> None:
        ...
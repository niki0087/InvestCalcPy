"""ORM модели для SQLAlchemy."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from data.local.database import Base


class DealModel(Base):
    __tablename__ = 'deals'

    deal_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    ticker: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_share: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    commission: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal('0'))
    is_buy: Mapped[bool] = mapped_column(Boolean, default=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
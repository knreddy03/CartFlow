from enum import Enum
from uuid import UUID

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(BaseModel):
    __tablename__ = "orders"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True,)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus, name="order_status"), default=OrderStatus.PENDING, nullable=False, index=True,)
    subtotal: Mapped[int] = mapped_column(Integer, nullable=False,)
    tax: Mapped[int] = mapped_column(Integer, nullable=False,)
    shipping_cost: Mapped[int] = mapped_column(Integer, nullable=False,)
    total: Mapped[int] = mapped_column(Integer, nullable=False,)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False,)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan",)
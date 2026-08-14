from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel


class Cart(BaseModel):
    __tablename__ = "carts"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False, index=True,)

    user = relationship("User", back_populates="cart", uselist=False)
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan",)

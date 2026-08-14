from uuid import UUID

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    cart_id: Mapped[UUID] = mapped_column(ForeignKey("carts.id"), nullable=False, index=True,)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False, index=True,)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False,)

    cart = relationship("Cart", back_populates="items",)
    product = relationship("Product", back_populates="cart_items",)

    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_items_cart_product",),
    )
    
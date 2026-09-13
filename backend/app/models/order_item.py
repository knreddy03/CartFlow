from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True,)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False, index=True,)
    variant_id: Mapped[UUID | None] = mapped_column(ForeignKey("product_variants.id"), nullable=True, index=True,)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False,)
    sku: Mapped[str | None] = mapped_column(String(100), nullable=True,)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False,)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False,)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False,)

    order = relationship("Order",back_populates="items",)
    product = relationship("Product")
    variant = relationship("ProductVariant")
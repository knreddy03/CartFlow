from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel


class ProductVariant(BaseModel):
    __tablename__ = "product_variants"

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="ck_product_variants_price_non_negative",
        ),
        CheckConstraint(
            "stock_quantity >= 0",
            name="ck_product_variants_stock_non_negative",
        ),
    )

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False, index=True,)
    sku: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False,)
    size: Mapped[str | None] = mapped_column(String(50), nullable=True,)
    color: Mapped[str | None] = mapped_column(String(50), nullable=True,)
    material: Mapped[str | None] = mapped_column(String(100), nullable=True,)
    # Stored in cents. Example: $19.99 -> 1999
    price: Mapped[int] = mapped_column(Integer, nullable=False,)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False,)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False,)

    product = relationship("Product", back_populates="variants",)
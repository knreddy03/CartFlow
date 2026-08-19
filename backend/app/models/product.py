from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_products_price_non_negative"),
        CheckConstraint("stock_quantity >= 0",name="ck_products_stock_non_negative",),
    )

    sub_category_id: Mapped[UUID] = mapped_column(ForeignKey("sub_categories.id"), index=True, nullable=False, )
    name: Mapped[str] = mapped_column(String(100), nullable=False, )
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, )
    description: Mapped[str | None] = mapped_column(String(500), nullable=True, )
    # Stored in cents. Example: $19.99 -> 1999
    price: Mapped[int] = mapped_column(Integer, nullable=False, )
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False, )
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, )
    image_url: Mapped[str] = mapped_column(String(255), nullable=False, )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, )

    sub_category = relationship("SubCategory", back_populates="products")
    cart_items = relationship("CartItem",back_populates="product",)
    
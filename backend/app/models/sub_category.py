from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel


class SubCategory(BaseModel):
    __tablename__ = "sub_categories"

    __table_args__ = (
        UniqueConstraint(
            "category_id",
            "slug",
            name="uq_sub_categories_category_slug",
        ),
    )

    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"), index=True, nullable=False,)
    name: Mapped[str] = mapped_column(String(100), nullable=False,)
    slug: Mapped[str] = mapped_column(String(100), nullable=False,)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True,)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True,)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True, nullable=False,)

    category = relationship("Category", back_populates="sub_categories",)
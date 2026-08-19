from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.product import Product


class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, product: Product) -> None:
        self.db.add(product)

    def get_by_id(self, product_id: UUID) -> Product | None:
        return self.db.get(Product, product_id)

    def get_by_name(self, name: str) -> Product | None:
        stmt = select(Product).where(Product.name == name)
        return self.db.scalar(stmt)

    def get_by_slug(self, slug: str) -> Product | None:
        stmt = select(Product).where(Product.slug == slug)
        return self.db.scalar(stmt)

    def get_products(
        self,
        sub_category_id: UUID | None = None,
        is_active: bool | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Product], int]:

        stmt = select(Product)
        count_stmt = select(func.count()).select_from(Product)

        if sub_category_id is not None:
            stmt = stmt.where(
                Product.sub_category_id == sub_category_id
            )
            count_stmt = count_stmt.where(
                Product.sub_category_id == sub_category_id
            )

        if is_active is not None:
            stmt = stmt.where(Product.is_active == is_active)
            count_stmt = count_stmt.where(Product.is_active == is_active)

        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
            count_stmt = count_stmt.where(Product.price >= min_price)

        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)
            count_stmt = count_stmt.where(Product.price <= max_price)

        stmt = (
            stmt
            .order_by(Product.name)
            .offset(offset)
            .limit(limit)
        )

        products = list(self.db.scalars(stmt).all())
        total = self.db.scalar(count_stmt) or 0

        return products, total

    def delete(self, product: Product) -> None:
        self.db.delete(product)
    
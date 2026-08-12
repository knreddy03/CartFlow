from uuid import UUID
from sqlalchemy import select
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
    
    def get_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.name)
        return list(self.db.scalars(stmt).all())

    def get_by_category(self, category_id: UUID) -> list[Product]:
        stmt = select(Product).where(Product.category_id == category_id).order_by(Product.name)
        return list(self.db.scalars(stmt).all())

    def delete(self, product: Product) -> None:
            self.db.delete(product)
    
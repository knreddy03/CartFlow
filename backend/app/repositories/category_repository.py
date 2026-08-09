from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, category: Category) -> None:
        self.db.add(category)

    def get_by_id(self, category_id: UUID) -> Category | None:
        return self.db.get(Category, category_id)

    def get_by_name(self, name: str) -> Category | None:
        stmt = select(Category).where(Category.name == name)
        return self.db.scalar(stmt)

    def get_by_slug(self, slug: str) -> Category | None:
        stmt = select(Category).where(Category.slug == slug)
        return self.db.scalar(stmt)
    
    def get_all(self) -> list[Category]:
        stmt = select(Category).order_by(Category.name)
        return list(self.db.scalars(stmt).all())

    def delete(self, category: Category) -> None:
        self.db.delete(category)
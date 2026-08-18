from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sub_category import SubCategory


class SubCategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, sub_category: SubCategory) -> None:
        self.db.add(sub_category)

    def get_by_id(self, sub_category_id: UUID) -> SubCategory | None:
        return self.db.get(SubCategory, sub_category_id)

    def get_by_category_and_name(self, category_id: UUID, name: str,) -> SubCategory | None:
        stmt = select(SubCategory).where(SubCategory.category_id == category_id,SubCategory.name == name,)
        return self.db.scalar(stmt)

    def get_by_category_and_slug(self, category_id: UUID, slug: str,) -> SubCategory | None:
        stmt = select(SubCategory).where(SubCategory.category_id == category_id,SubCategory.slug == slug,)
        return self.db.scalar(stmt)
    
    def get_by_category(self, category_id: UUID) -> list[SubCategory]:
        stmt = select(SubCategory).where(SubCategory.category_id == category_id).order_by(SubCategory.name)
        return list(self.db.scalars(stmt).all())

    def get_all(self) -> list[SubCategory]:
            stmt = select(SubCategory).order_by(SubCategory.name)
            return list(self.db.scalars(stmt).all())

    def delete(self, sub_category: SubCategory) -> None:
        self.db.delete(sub_category)
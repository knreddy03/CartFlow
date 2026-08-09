from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.category_exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
)
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


class CategoryService:

    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def create_category(self, category_data: CategoryCreate) -> Category:
        existing_name = self.category_repository.get_by_name(category_data.name)

        if existing_name is not None:
            raise CategoryAlreadyExistsError(
                "Category with this name already exists."
            )

        existing_slug = self.category_repository.get_by_slug(category_data.slug)

        if existing_slug is not None:
            raise CategoryAlreadyExistsError(
                "Category with this slug already exists."
            )

        category = Category(
            name=category_data.name,
            slug=category_data.slug,
            description=category_data.description,
            image_url=category_data.image_url,
            is_active=category_data.is_active,
        )

        try:
            self.category_repository.add(category)

            self.db.commit()
            self.db.refresh(category)

            return category

        except Exception:
            self.db.rollback()
            raise

    def get_category_by_id(self, category_id: UUID) -> Category:
        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError("Category not found.")

        return category

    def get_category_by_name(self, name: str) -> Category | None:
        return self.category_repository.get_by_name(name)

    def get_all_categories(self) -> list[Category]:
        return self.category_repository.get_all()

    def update_category(
        self,
        category_id: UUID,
        category_data: CategoryUpdate,
    ) -> Category:

        category = self.get_category_by_id(category_id)

        update_data = category_data.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing_category = self.category_repository.get_by_name(
                update_data["name"]
            )

            if (
                existing_category is not None
                and existing_category.id != category_id
            ):
                raise CategoryAlreadyExistsError(
                    "Category with this name already exists."
                )

        if "slug" in update_data:
            existing_category = self.category_repository.get_by_slug(
                update_data["slug"]
            )

            if (
                existing_category is not None
                and existing_category.id != category_id
            ):
                raise CategoryAlreadyExistsError(
                    "Category with this slug already exists."
                )

        try:
            for field, value in update_data.items():
                setattr(category, field, value)

            self.db.commit()
            self.db.refresh(category)

            return category

        except Exception:
            self.db.rollback()
            raise

    def delete_category(self, category_id: UUID) -> None:
        category = self.get_category_by_id(category_id)

        try:
            self.category_repository.delete(category)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
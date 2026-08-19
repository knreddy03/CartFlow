from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.category_exceptions import CategoryNotFoundError
from app.exceptions.sub_category_exceptions import (
    SubCategoryAlreadyExistsError,
    SubCategoryNotFoundError,
)
from app.models.sub_category import SubCategory
from app.repositories.category_repository import CategoryRepository
from app.repositories.sub_category_repository import SubCategoryRepository
from app.schemas.sub_category_schema import (
    SubCategoryCreate,
    SubCategoryUpdate,
)


class SubCategoryService:

    def __init__(self, db: Session):
        self.db = db
        self.sub_category_repository = SubCategoryRepository(db)
        self.category_repository = CategoryRepository(db)

    def create_sub_category(
        self,
        sub_category_data: SubCategoryCreate,
    ) -> SubCategory:

        # Verify parent category exists.
        category = self.category_repository.get_by_id(
            sub_category_data.category_id
        )

        if category is None:
            raise CategoryNotFoundError("Category not found.")

        # Name must be unique within the parent category.
        existing_name = (
            self.sub_category_repository.get_by_category_and_name(
                sub_category_data.category_id,
                sub_category_data.name,
            )
        )

        if existing_name is not None:
            raise SubCategoryAlreadyExistsError(
                "Sub Category with this name already exists."
            )

        # Slug must be unique within the parent category.
        existing_slug = (
            self.sub_category_repository.get_by_category_and_slug(
                sub_category_data.category_id,
                sub_category_data.slug,
            )
        )

        if existing_slug is not None:
            raise SubCategoryAlreadyExistsError(
                "Sub Category with this slug already exists."
            )

        sub_category = SubCategory(
            category_id=sub_category_data.category_id,
            name=sub_category_data.name,
            slug=sub_category_data.slug,
            description=sub_category_data.description,
            image_url=sub_category_data.image_url,
            is_active=sub_category_data.is_active,
        )

        try:
            self.sub_category_repository.add(sub_category)

            self.db.commit()
            self.db.refresh(sub_category)

            return sub_category

        except Exception:
            self.db.rollback()
            raise

    def get_sub_category_by_id(
        self,
        sub_category_id: UUID,
    ) -> SubCategory:

        sub_category = self.sub_category_repository.get_by_id(
            sub_category_id
        )

        if sub_category is None:
            raise SubCategoryNotFoundError(
                "Sub Category not found."
            )

        return sub_category

    def get_all_sub_categories(self) -> list[SubCategory]:
        return self.sub_category_repository.get_all()

    def get_sub_categories_by_category(
        self,
        category_id: UUID,
    ) -> list[SubCategory]:

        # Verify parent category exists.
        category = self.category_repository.get_by_id(
            category_id
        )

        if category is None:
            raise CategoryNotFoundError(
                "Category not found."
            )

        return self.sub_category_repository.get_by_category(
            category_id
        )

    def update_sub_category(
        self,
        sub_category_id: UUID,
        sub_category_data: SubCategoryUpdate,
    ) -> SubCategory:

        sub_category = self.get_sub_category_by_id(
            sub_category_id
        )

        update_data = sub_category_data.model_dump(
            exclude_unset=True
        )

        # Determine the category the sub-category will belong to
        # after the update.
        target_category_id = update_data.get(
            "category_id",
            sub_category.category_id,
        )

        # If category_id is being changed, verify the new
        # parent category exists.
        if "category_id" in update_data:
            category = self.category_repository.get_by_id(
                update_data["category_id"]
            )

            if category is None:
                raise CategoryNotFoundError(
                    "Category not found."
                )

        # Check name uniqueness within the target category.
        if "name" in update_data:
            existing_sub_category = (
                self.sub_category_repository.get_by_category_and_name(
                    target_category_id,
                    update_data["name"],
                )
            )

            if (
                existing_sub_category is not None
                and existing_sub_category.id != sub_category_id
            ):
                raise SubCategoryAlreadyExistsError(
                    "Sub Category with this name already exists."
                )

        # Check slug uniqueness within the target category.
        if "slug" in update_data:
            existing_sub_category = (
                self.sub_category_repository.get_by_category_and_slug(
                    target_category_id,
                    update_data["slug"],
                )
            )

            if (
                existing_sub_category is not None
                and existing_sub_category.id != sub_category_id
            ):
                raise SubCategoryAlreadyExistsError(
                    "Sub Category with this slug already exists."
                )

        try:
            for field, value in update_data.items():
                setattr(sub_category, field, value)

            self.db.commit()
            self.db.refresh(sub_category)

            return sub_category

        except Exception:
            self.db.rollback()
            raise

    def delete_sub_category(
        self,
        sub_category_id: UUID,
    ) -> None:

        sub_category = self.get_sub_category_by_id(
            sub_category_id
        )

        try:
            self.sub_category_repository.delete(
                sub_category
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
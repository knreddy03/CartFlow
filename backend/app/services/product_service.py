from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.category_exceptions import CategoryNotFoundError
from app.exceptions.product_exceptions import (
    ProductAlreadyExistsError,
    ProductNotFoundError,
)
from app.models.product import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductService:

    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def create_product(self, product_data: ProductCreate) -> Product:

        category = self.category_repository.get_by_id(
            product_data.category_id
        )

        if category is None:
            raise CategoryNotFoundError("Category not found.")

        existing_name = self.product_repository.get_by_name(
            product_data.name
        )

        if existing_name is not None:
            raise ProductAlreadyExistsError(
                "Product with this name already exists."
            )

        existing_slug = self.product_repository.get_by_slug(
            product_data.slug
        )

        if existing_slug is not None:
            raise ProductAlreadyExistsError(
                "Product with this slug already exists."
            )

        product = Product(
            category_id=product_data.category_id,
            name=product_data.name,
            slug=product_data.slug,
            description=product_data.description,
            price=product_data.price,
            currency=product_data.currency,
            stock_quantity=product_data.stock_quantity,
            image_url=product_data.image_url,
            is_active=product_data.is_active,
        )

        try:
            self.product_repository.add(product)

            self.db.commit()
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    def get_product_by_id(self, product_id: UUID) -> Product:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError("Product not found.")

        return product

    def get_product_by_name(self, name: str) -> Product | None:
        return self.product_repository.get_by_name(name)

    def get_all_products(self) -> list[Product]:
        return self.product_repository.get_all()

    def get_products_by_category(
        self,
        category_id: UUID,
    ) -> list[Product]:
        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError("Category not found.")

        return self.product_repository.get_by_category(category_id)

    def update_product(
        self,
        product_id: UUID,
        product_data: ProductUpdate,
    ) -> Product:

        product = self.get_product_by_id(product_id)

        update_data = product_data.model_dump(exclude_unset=True)

        if "category_id" in update_data:
            category = self.category_repository.get_by_id(
                update_data["category_id"]
            )

            if category is None:
                raise CategoryNotFoundError("Category not found.")

        if "name" in update_data:
            existing_product = self.product_repository.get_by_name(
                update_data["name"]
            )

            if (
                existing_product is not None
                and existing_product.id != product_id
            ):
                raise ProductAlreadyExistsError(
                    "Product with this name already exists."
                )

        if "slug" in update_data:
            existing_product = self.product_repository.get_by_slug(
                update_data["slug"]
            )

            if (
                existing_product is not None
                and existing_product.id != product_id
            ):
                raise ProductAlreadyExistsError(
                    "Product with this slug already exists."
                )

        try:
            for field, value in update_data.items():
                setattr(product, field, value)

            self.db.commit()
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    def delete_product(self, product_id: UUID) -> None:
        product = self.get_product_by_id(product_id)

        try:
            self.product_repository.delete(product)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
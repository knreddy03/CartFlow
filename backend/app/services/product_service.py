from math import ceil
from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.sub_category_exceptions import SubCategoryNotFoundError
from app.exceptions.product_exceptions import (
    ProductAlreadyExistsError,
    ProductNotFoundError,
    MinPriceGreaterThanMaxPriceError,
)
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.sub_category_repository import SubCategoryRepository
from app.schemas.product_schema import (
    ProductCreate,
    ProductListResponse,
    ProductUpdate,
)


class ProductService:

    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.sub_category_repository = SubCategoryRepository(db)

    def create_product(self, product_data: ProductCreate) -> Product:

        sub_category = self.sub_category_repository.get_by_id(
            product_data.sub_category_id
        )

        if sub_category is None:
            raise SubCategoryNotFoundError("Sub Category not found.")

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
            sub_category_id=product_data.sub_category_id,
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

    def get_products(
        self,
        sub_category_id: UUID | None = None,
        is_active: bool | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> ProductListResponse:

        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise MinPriceGreaterThanMaxPriceError(
                    "min_price cannot be greater than max_price."
                )

        if sub_category_id is not None:
            sub_category = self.sub_category_repository.get_by_id(
                sub_category_id
            )

            if sub_category is None:
                raise SubCategoryNotFoundError(
                    "Sub Category not found."
                )

        offset = (page - 1) * page_size

        products, total = self.product_repository.get_products(
            sub_category_id=sub_category_id,
            is_active=is_active,
            min_price=min_price,
            max_price=max_price,
            offset=offset,
            limit=page_size,
        )

        total_pages = ceil(total / page_size) if total > 0 else 0

        return ProductListResponse(
            items=products,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def update_product(
        self,
        product_id: UUID,
        product_data: ProductUpdate,
    ) -> Product:

        product = self.get_product_by_id(product_id)

        update_data = product_data.model_dump(exclude_unset=True)

        if "sub_category_id" in update_data:
            sub_category = self.sub_category_repository.get_by_id(
                update_data["sub_category_id"]
            )

            if sub_category is None:
                raise SubCategoryNotFoundError(
                    "Sub Category not found."
                )

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
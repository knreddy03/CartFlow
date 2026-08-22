from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.product_exceptions import ProductNotFoundError
from app.exceptions.product_variant_exceptions import (
    ProductVariantAlreadyExistsError,
    ProductVariantNotFoundError,
)
from app.models.product_variant import ProductVariant
from app.repositories.product_repository import ProductRepository
from app.repositories.product_variant_repository import ProductVariantRepository
from app.schemas.product_variant_schema import (
    ProductVariantCreate,
    ProductVariantUpdate,
)


class ProductVariantService:

    def __init__(self, db: Session):
        self.db = db
        self.product_variant_repository = ProductVariantRepository(db)
        self.product_repository = ProductRepository(db)

    def create_product_variant(
        self,
        product_id: UUID,
        product_variant_data: ProductVariantCreate,
    ) -> ProductVariant:

        # Verify that the product exists.
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError("Product not found.")

        # SKU must be unique.
        existing_variant = self.product_variant_repository.get_by_sku(
            product_variant_data.sku
        )

        if existing_variant is not None:
            raise ProductVariantAlreadyExistsError(
                "Product variant with this SKU already exists."
            )

        product_variant = ProductVariant(
            product_id=product_id,
            sku=product_variant_data.sku,
            size=product_variant_data.size,
            color=product_variant_data.color,
            material=product_variant_data.material,
            price=product_variant_data.price,
            stock_quantity=product_variant_data.stock_quantity,
            is_active=product_variant_data.is_active,
        )

        try:
            self.product_variant_repository.add(product_variant)

            self.db.commit()
            self.db.refresh(product_variant)

            return product_variant

        except Exception:
            self.db.rollback()
            raise

    def get_product_variant_by_id(
        self,
        product_id: UUID,
        product_variant_id: UUID,
    ) -> ProductVariant:

        # First make sure the product exists.
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError("Product not found.")

        variant = self.product_variant_repository.get_by_id(
            product_variant_id
        )

        if variant is None or variant.product_id != product_id:
            raise ProductVariantNotFoundError(
                "Product variant not found."
            )

        return variant

    def get_product_variants(
        self,
        product_id: UUID,
    ) -> list[ProductVariant]:

        # Verify that the product exists.
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError("Product not found.")

        return self.product_variant_repository.get_by_product(
            product_id
        )

    def update_product_variant(
        self,
        product_id: UUID,
        product_variant_id: UUID,
        product_variant_data: ProductVariantUpdate,
    ) -> ProductVariant:

        variant = self.get_product_variant_by_id(
            product_id,
            product_variant_id,
        )

        update_data = product_variant_data.model_dump(
            exclude_unset=True
        )

        # Check SKU uniqueness if SKU is being changed.
        if "sku" in update_data:
            existing_variant = (
                self.product_variant_repository.get_by_sku(
                    update_data["sku"]
                )
            )

            if (
                existing_variant is not None
                and existing_variant.id != product_variant_id
            ):
                raise ProductVariantAlreadyExistsError(
                    "Product variant with this SKU already exists."
                )

        try:
            for field, value in update_data.items():
                setattr(variant, field, value)

            self.db.commit()
            self.db.refresh(variant)

            return variant

        except Exception:
            self.db.rollback()
            raise

    def delete_product_variant(
        self,
        product_id: UUID,
        product_variant_id: UUID,
    ) -> None:

        variant = self.get_product_variant_by_id(
            product_id,
            product_variant_id,
        )

        try:
            self.product_variant_repository.delete(variant)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
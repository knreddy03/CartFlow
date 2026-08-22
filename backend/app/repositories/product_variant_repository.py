from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.product_variant import ProductVariant


class ProductVariantRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, product_variant: ProductVariant) -> None:
        self.db.add(product_variant)

    def get_by_id(self, product_variant_id: UUID) -> ProductVariant | None:
        return self.db.get(ProductVariant, product_variant_id)

    def get_by_sku(self, sku: str) -> ProductVariant | None:
            stmt = select(ProductVariant).where(ProductVariant.sku == sku)
            return self.db.scalar(stmt)
    
    def get_by_product(self, product_id: UUID) -> list[ProductVariant]:
        stmt = select(ProductVariant).where(ProductVariant.product_id == product_id).order_by(ProductVariant.sku)
        return list(self.db.scalars(stmt).all())

    def delete(self, product: ProductVariant) -> None:
        self.db.delete(product)
    
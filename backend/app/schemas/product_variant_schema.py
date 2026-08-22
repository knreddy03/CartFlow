from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductVariantBase(BaseModel):
    sku: str = Field(..., min_length=2, max_length=100,)
    size: str | None = Field(default=None, min_length=1, max_length=50,)
    color: str | None = Field(default=None, min_length=1, max_length=50,)
    material: str | None = Field(default=None, min_length=1, max_length=100,)
    price: int = Field(..., ge=0,)
    stock_quantity: int = Field(..., ge=0,)
    is_active: bool = True


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantUpdate(BaseModel):
    sku: str | None = Field(default=None, min_length=2, max_length=100,)
    size: str | None = Field(default=None, min_length=1, max_length=50,)
    color: str | None = Field(default=None, min_length=1, max_length=50,)
    material: str | None = Field(default=None, min_length=1, max_length=100,)
    price: int | None = Field(default=None, ge=0,)
    stock_quantity: int | None = Field(default=None, ge=0,)
    is_active: bool | None = None


class ProductVariantResponse(ProductVariantBase):
    id: UUID
    product_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
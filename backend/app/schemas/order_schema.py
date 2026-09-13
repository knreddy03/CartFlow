from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.order import OrderStatus


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    variant_id: UUID | None
    product_name: str
    sku: str | None
    quantity: int
    unit_price: int
    total_price: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: OrderStatus
    subtotal: int
    tax: int
    shipping_cost: int
    total: int
    currency: str
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
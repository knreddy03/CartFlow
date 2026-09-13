from uuid import UUID

from sqlalchemy.orm import Session

from app.models.order_item import OrderItem


class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, order_item: OrderItem) -> None:
        self.db.add(order_item)

    def get_by_id(self, order_item_id: UUID) -> OrderItem | None:
        return self.db.get(OrderItem, order_item_id)

    def get_by_order_id(self, order_id: UUID) -> list[OrderItem]:
        return (
            self.db.query(OrderItem)
            .filter(OrderItem.order_id == order_id)
            .all()
        )

    def delete(self, order_item: OrderItem) -> None:
        self.db.delete(order_item)
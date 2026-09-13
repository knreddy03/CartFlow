from uuid import UUID

from sqlalchemy.orm import Session

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, order: Order) -> None:
        self.db.add(order)

    def get_by_id(self, order_id: UUID) -> Order | None:
        return self.db.get(Order, order_id)

    def get_by_user_id(self, user_id: UUID) -> list[Order]:
        return (
            self.db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def delete(self, order: Order) -> None:
        self.db.delete(order)
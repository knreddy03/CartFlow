from uuid import UUID
from sqlalchemy.orm import Session
from app.models.cart import Cart


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, cart_id: UUID) -> Cart | None:
        return self.db.get(Cart, cart_id)

    def get_by_user_id(self, user_id: UUID) -> Cart | None:
        return (
            self.db.query(Cart)
            .filter(Cart.user_id == user_id)
            .first()
        )

    def create(self, cart: Cart) -> Cart:
        self.db.add(cart)
        return cart

    def delete(self, cart: Cart) -> None:
        self.db.delete(cart)
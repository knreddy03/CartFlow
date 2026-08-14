from uuid import UUID
from sqlalchemy.orm import Session
from app.models.cart_item import CartItem


class CartItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, cart_item_id: UUID) -> CartItem | None:
        return self.db.get(CartItem, cart_item_id)

    def get_by_cart_and_product(
        self,
        cart_id: UUID,
        product_id: UUID,
    ) -> CartItem | None:
        return (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
            .first()
        )

    def get_by_cart_id(self, cart_id: UUID) -> list[CartItem]:
        return (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart_id)
            .all()
        )

    def create(self, cart_item: CartItem) -> CartItem:
        self.db.add(cart_item)
        return cart_item

    def delete(self, cart_item: CartItem) -> None:
        self.db.delete(cart_item)
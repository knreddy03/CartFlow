from uuid import UUID
from sqlalchemy.orm import Session
from app.models.cart_item import CartItem


class CartItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, cart_item_id: UUID) -> CartItem | None:
        return self.db.get(CartItem, cart_item_id)

    def get_by_cart_product_variant(
        self,
        cart_id: UUID,
        product_id: UUID,
        variant_id: UUID | None
    ) -> CartItem | None:
        query = (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
        )

        if variant_id is None:
            query = query.filter(CartItem.variant_id.is_(None))
        else:
            query = query.filter(CartItem.variant_id == variant_id)

        return query.first()

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
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.repositories.cart_repository import CartRepository
from app.repositories.cart_item_repository import CartItemRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart_schema import (
    CartItemCreate,
    CartItemUpdate,
)
from app.exceptions.cart_exceptions import (
    CartNotFoundError,
    CartItemNotFoundError,
    ProductOutOfStockError,
    InsufficientStockError,

)
from app.exceptions.product_exceptions import ProductNotFoundError


class CartService:
    def __init__(
        self,
        db: Session,
        cart_repository: CartRepository,
        cart_item_repository: CartItemRepository,
        product_repository: ProductRepository,
    ):
        self.db = db
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    def get_or_create_cart(self, user_id: UUID) -> Cart:
        cart = self.cart_repository.get_by_user_id(user_id)

        if cart:
            return cart

        cart = Cart(user_id=user_id)
        self.cart_repository.create(cart)

        self.db.flush()

        return cart

    def get_cart(self, user_id: UUID) -> Cart:
        return self.get_or_create_cart(user_id)

    def add_item(
        self,
        user_id: UUID,
        item_data: CartItemCreate,
    ) -> CartItem:
        product = self.product_repository.get_by_id(
            item_data.product_id
        )

        if product is None or not product.is_active:
            raise ProductNotFoundError("Product not found.")

        if product.stock_quantity <= 0:
            raise ProductOutOfStockError("Product is out of stock.")

        cart = self.get_or_create_cart(user_id)

        existing_item = (
            self.cart_item_repository.get_by_cart_and_product(
                cart.id,
                item_data.product_id,
            )
        )

        current_quantity = (
            existing_item.quantity
            if existing_item
            else 0
        )

        requested_quantity = current_quantity + item_data.quantity

        if requested_quantity > product.stock_quantity:
            raise InsufficientStockError(
                "Requested quantity exceeds available stock."
            )
    
        if existing_item:
            existing_item.quantity = requested_quantity

            try:
                self.db.commit()
                self.db.refresh(existing_item)
            except Exception:
                self.db.rollback()
                raise

            return existing_item

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
        )

        self.cart_item_repository.create(cart_item)

        try:
            self.db.commit()
            self.db.refresh(cart_item)
        except Exception:
            self.db.rollback()
            raise

        return cart_item

    def update_item(
        self,
        user_id: UUID,
        cart_item_id: UUID,
        item_data: CartItemUpdate,
    ) -> CartItem:
        cart = self.cart_repository.get_by_user_id(user_id)

        if cart is None:
            raise CartNotFoundError("Cart not found.")

        cart_item = self.cart_item_repository.get_by_id(
            cart_item_id
        )

        if cart_item is None or cart_item.cart_id != cart.id:
            raise CartItemNotFoundError("Cart item not found.")

        product = self.product_repository.get_by_id(cart_item.product_id)

        if product is None or not product.is_active:
            raise ProductNotFoundError("Product not found.")

        if product.stock_quantity <= 0:
            raise ProductOutOfStockError("Product is out of stock.")

        if item_data.quantity > product.stock_quantity:
            raise InsufficientStockError("Requested quantity exceeds available stock.")
        
        cart_item.quantity = item_data.quantity
        
        try:
            self.db.commit()
            self.db.refresh(cart_item)
        except Exception:
            self.db.rollback()
            raise

        return cart_item

    def remove_item(
        self,
        user_id: UUID,
        cart_item_id: UUID,
    ) -> None:
        cart = self.cart_repository.get_by_user_id(user_id)

        if cart is None:
            raise CartNotFoundError("Cart not found.")

        cart_item = self.cart_item_repository.get_by_id(
            cart_item_id
        )

        if cart_item is None or cart_item.cart_id != cart.id:
            raise CartItemNotFoundError("Cart item not found.")

        self.cart_item_repository.delete(cart_item)

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
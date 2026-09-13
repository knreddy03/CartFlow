from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.cart_exceptions import (
    CartEmptyError,
    CartNotFoundError,
    InsufficientStockError,
    ProductOutOfStockError,
)
from app.exceptions.product_exceptions import ProductNotFoundError
from app.exceptions.product_variant_exceptions import (
    ProductVariantNotFoundError,
)
from app.exceptions.order_exceptions import (
    OrderNotFoundError,
    InvalidOrderStatusTransitionError,
)

from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem

from app.repositories.cart_item_repository import CartItemRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.product_variant_repository import (
    ProductVariantRepository,
)


VALID_STATUS_TRANSITIONS = {
    OrderStatus.PENDING: {
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.CONFIRMED: {
        OrderStatus.PROCESSING,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PROCESSING: {
        OrderStatus.SHIPPED,
    },
    OrderStatus.SHIPPED: {
        OrderStatus.DELIVERED,
    },
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}

class OrderService:
    def __init__(
        self,
        db: Session,
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
        cart_repository: CartRepository,
        cart_item_repository: CartItemRepository,
        product_repository: ProductRepository,
        product_variant_repository: ProductVariantRepository,
    ):
        self.db = db
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository
        self.product_variant_repository = product_variant_repository

    def create_order(self, user_id: UUID) -> Order:
        try:
            cart = self.cart_repository.get_by_user_id(user_id)

            if cart is None:
                raise CartNotFoundError("Cart not found.")

            cart_items = self.cart_item_repository.get_by_cart_id(cart.id)

            if not cart_items:
                raise CartEmptyError("Cart is empty.")

            subtotal = 0
            order_items: list[OrderItem] = []
            inventory_updates: list[tuple[Product | ProductVariant, int]] = []

            for cart_item in cart_items:
                product = self.product_repository.get_by_id(
                    cart_item.product_id
                )

                if product is None or not product.is_active:
                    raise ProductNotFoundError("Product not found.")

                variant = None

                if cart_item.variant_id is not None:
                    variant = self.product_variant_repository.get_by_id(
                        cart_item.variant_id
                    )

                    if variant is None or variant.product_id != product.id:
                        raise ProductVariantNotFoundError(
                            "Product variant not found."
                        )

                    if not variant.is_active:
                        raise ProductVariantNotFoundError(
                            "Product variant not found."
                        )

                    available_stock = variant.stock_quantity
                    unit_price = variant.price
                    sku = variant.sku
                    inventory_object = variant

                else:
                    available_stock = product.stock_quantity
                    unit_price = product.price
                    sku = None
                    inventory_object = product

                if available_stock <= 0:
                    raise ProductOutOfStockError(
                        "Product is out of stock."
                    )

                if cart_item.quantity > available_stock:
                    raise InsufficientStockError(
                        "Requested quantity exceeds available stock."
                    )

                item_total = unit_price * cart_item.quantity
                subtotal += item_total

                order_items.append(
                    OrderItem(
                        product_id=product.id,
                        variant_id=variant.id if variant else None,
                        product_name=product.name,
                        sku=sku,
                        quantity=cart_item.quantity,
                        unit_price=unit_price,
                        total_price=item_total,
                    )
                )

                inventory_updates.append(
                    (inventory_object, cart_item.quantity)
                )

            tax = 0
            shipping_cost = 0
            total = subtotal + tax + shipping_cost

            order = Order(
                user_id=user_id,
                status=OrderStatus.PENDING,
                subtotal=subtotal,
                tax=tax,
                shipping_cost=shipping_cost,
                total=total,
                currency="USD",
            )

            self.order_repository.add(order)

            self.db.flush()

            for order_item in order_items:
                order_item.order_id = order.id
                self.order_item_repository.add(order_item)

            for inventory_object, quantity in inventory_updates:
                inventory_object.stock_quantity -= quantity

            for cart_item in cart_items:
                self.cart_item_repository.delete(cart_item)

            self.db.commit()
            self.db.refresh(order)

            return order

        except Exception:
            self.db.rollback()
            raise


    def update_order_status(
        self,
        order_id: UUID,
        new_status: OrderStatus,
    ) -> Order:
        try:
            order = self.order_repository.get_by_id(order_id)

            if order is None:
                raise OrderNotFoundError("Order not found.")

            allowed_statuses = VALID_STATUS_TRANSITIONS[
                order.status
            ]

            if new_status not in allowed_statuses:
                raise InvalidOrderStatusTransitionError(
                    f"Cannot change order status from "
                    f"{order.status.value} to {new_status.value}."
                )

            order.status = new_status

            self.db.commit()
            self.db.refresh(order)

            return order

        except Exception:
            self.db.rollback()
            raise


    def get_user_orders(self, user_id: UUID) -> list[Order]:
        return self.order_repository.get_by_user_id(user_id)


    def get_order(
        self,
        order_id: UUID,
        user_id: UUID,
    ) -> Order:
        order = self.order_repository.get_by_id(order_id)

        if order is None or order.user_id != user_id:
            raise OrderNotFoundError("Order not found.")

        return order


    def cancel_order(
        self,
        order_id: UUID,
        user_id: UUID,
    ) -> Order:
        order = self.get_order(order_id, user_id)

        if OrderStatus.CANCELLED not in VALID_STATUS_TRANSITIONS[order.status]:
            raise InvalidOrderStatusTransitionError(
                f"Cannot cancel order from {order.status.value}."
            )

        order.status = OrderStatus.CANCELLED

        self.db.commit()
        self.db.refresh(order)

        return order
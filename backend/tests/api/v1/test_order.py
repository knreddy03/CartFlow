from uuid import uuid4
from datetime import date

import pytest

from app.models.user import User, UserRole

from app.exceptions.cart_exceptions import (
    CartEmptyError,
    CartNotFoundError,
    InsufficientStockError,
    ProductOutOfStockError,
)
from app.exceptions.product_exceptions import ProductNotFoundError
from app.exceptions.product_variant_exceptions import ProductVariantNotFoundError
from app.exceptions.order_exceptions import (
    InvalidOrderStatusTransitionError, 
    OrderNotFoundError,
)

from app.models.category import Category
from app.models.sub_category import SubCategory
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem

from app.repositories.cart_item_repository import CartItemRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.product_variant_repository import ProductVariantRepository

from app.services.order_service import OrderService


def create_product(db_session):
    category = Category(
        name="Men",
        slug="men",
        description="Men's clothing",
        image_url="https://example.com/images/men.jpg",
        is_active=True,
    )

    db_session.add(category)
    db_session.flush()

    sub_category = SubCategory(
        category_id=category.id,
        name="Shirts",
        slug="shirts",
        description="Men's shirts",
        image_url="https://example.com/images/shirts.jpg",
        is_active=True,
    )

    db_session.add(sub_category)
    db_session.flush()

    product = Product(
        sub_category_id=sub_category.id,
        name="Classic Shirt",
        slug="classic-shirt",
        description="Classic men's shirt",
        price=2499,
        currency="USD",
        stock_quantity=25,
        image_url="https://example.com/images/classic-shirt.jpg",
        is_active=True,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product


# -------------------------
# Order Repository
# -------------------------


def test_add_and_get_order(db_session, authenticated_user):
    repository = OrderRepository(db_session)

    order = Order(
        user_id=authenticated_user.id,
        status=OrderStatus.PENDING,
        subtotal=4998,
        tax=500,
        shipping_cost=0,
        total=5498,
        currency="USD",
    )

    repository.add(order)
    db_session.commit()
    db_session.refresh(order)

    result = repository.get_by_id(order.id)

    assert result is not None
    assert result.id == order.id
    assert result.user_id == authenticated_user.id
    assert result.status == OrderStatus.PENDING
    assert result.subtotal == 4998
    assert result.total == 5498


def test_get_orders_by_user_id(db_session, authenticated_user):
    repository = OrderRepository(db_session)

    first_order = Order(
        user_id=authenticated_user.id,
        status=OrderStatus.PENDING,
        subtotal=1000,
        tax=100,
        shipping_cost=0,
        total=1100,
        currency="USD",
    )

    second_order = Order(
        user_id=authenticated_user.id,
        status=OrderStatus.CONFIRMED,
        subtotal=2000,
        tax=200,
        shipping_cost=500,
        total=2700,
        currency="USD",
    )

    repository.add(first_order)
    repository.add(second_order)
    db_session.commit()

    orders = repository.get_by_user_id(authenticated_user.id)

    assert len(orders) == 2
    assert {order.id for order in orders} == {
        first_order.id,
        second_order.id,
    }


def test_get_orders_by_user_id_returns_empty_list(
    db_session,
    authenticated_user,
):
    repository = OrderRepository(db_session)

    orders = repository.get_by_user_id(authenticated_user.id)

    assert orders == []


def test_delete_order(
    db_session,
    authenticated_user,
):
    repository = OrderRepository(db_session)

    order = Order(
        user_id=authenticated_user.id,
        status=OrderStatus.PENDING,
        subtotal=1000,
        tax=100,
        shipping_cost=0,
        total=1100,
        currency="USD",
    )

    repository.add(order)
    db_session.commit()

    order_id = order.id

    repository.delete(order)
    db_session.commit()

    result = repository.get_by_id(order_id)

    assert result is None


# -------------------------
# Order Item Repository
# -------------------------


def test_add_and_get_order_item(
    db_session,
    authenticated_user,
):
    order_repository = OrderRepository(db_session)
    item_repository = OrderItemRepository(db_session)

    product = create_product(db_session)

    order = Order(
        user_id=authenticated_user.id,
        status=OrderStatus.PENDING,
        subtotal=2499,
        tax=250,
        shipping_cost=0,
        total=2749,
        currency="USD",
    )

    order_repository.add(order)
    db_session.flush()

    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        variant_id=None,
        product_name=product.name,
        sku=None,
        quantity=1,
        unit_price=2499,
        total_price=2499,
    )

    item_repository.add(order_item)
    db_session.commit()
    db_session.refresh(order_item)

    result = item_repository.get_by_id(order_item.id)

    assert result is not None
    assert result.id == order_item.id
    assert result.order_id == order.id
    assert result.product_id == product.id
    assert result.variant_id is None
    assert result.product_name == "Classic Shirt"
    assert result.sku is None
    assert result.quantity == 1
    assert result.unit_price == 2499
    assert result.total_price == 2499


def test_get_order_items_by_order_id(
    db_session,
    authenticated_user,
):
    order_repository = OrderRepository(db_session)
    item_repository = OrderItemRepository(db_session)

    product = create_product(db_session)

    order = Order(
        user_id=authenticated_user.id,
        status=OrderStatus.CONFIRMED,
        subtotal=4998,
        tax=500,
        shipping_cost=0,
        total=5498,
        currency="USD",
    )

    order_repository.add(order)
    db_session.flush()

    first_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        product_name=product.name,
        sku=None,
        quantity=1,
        unit_price=2499,
        total_price=2499,
    )

    second_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        product_name=product.name,
        sku=None,
        quantity=1,
        unit_price=2499,
        total_price=2499,
    )

    item_repository.add(first_item)
    item_repository.add(second_item)
    db_session.commit()

    items = item_repository.get_by_order_id(order.id)

    assert len(items) == 2
    assert {item.id for item in items} == {
        first_item.id,
        second_item.id,
    }


def test_get_order_items_by_order_id_returns_empty_list(
    db_session,
):
    repository = OrderItemRepository(db_session)

    items = repository.get_by_order_id(uuid4())

    assert items == []


def test_delete_order_item(
    db_session,
    authenticated_user,
):
    order_repository = OrderRepository(db_session)
    item_repository = OrderItemRepository(db_session)

    product = create_product(db_session)

    order = Order(
        user_id=authenticated_user.id,
        status=OrderStatus.PENDING,
        subtotal=1000,
        tax=100,
        shipping_cost=0,
        total=1100,
        currency="USD",
    )

    order_repository.add(order)
    db_session.flush()

    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        product_name=product.name,
        sku=None,
        quantity=1,
        unit_price=1000,
        total_price=1000,
    )

    item_repository.add(order_item)
    db_session.commit()

    item_id = order_item.id

    item_repository.delete(order_item)
    db_session.commit()

    result = item_repository.get_by_id(item_id)

    assert result is None


def create_order_service(db_session):
    return OrderService(
        db=db_session,
        order_repository=OrderRepository(db_session),
        order_item_repository=OrderItemRepository(db_session),
        cart_repository=CartRepository(db_session),
        cart_item_repository=CartItemRepository(db_session),
        product_repository=ProductRepository(db_session),
        product_variant_repository=ProductVariantRepository(db_session),
    )


def create_cart(db_session, user):
    cart = Cart(user_id=user.id)

    db_session.add(cart)
    db_session.flush()

    return cart


def create_cart_item(
    db_session,
    cart,
    product,
    quantity=1,
    variant=None,
):
    cart_item = CartItem(
        cart_id=cart.id,
        product_id=product.id,
        variant_id=variant.id if variant else None,
        quantity=quantity,
    )

    db_session.add(cart_item)
    db_session.commit()
    db_session.refresh(cart_item)

    return cart_item


# -------------------------
# Basic checkout
# -------------------------


def test_create_order_from_cart(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=2,
    )

    order = service.create_order(authenticated_user.id)

    assert order is not None
    assert order.user_id == authenticated_user.id
    assert order.status == OrderStatus.PENDING

    assert order.subtotal == product.price * 2
    assert order.tax == 0
    assert order.shipping_cost == 0
    assert order.total == product.price * 2
    assert order.currency == "USD"

    assert len(order.items) == 1

    order_item = order.items[0]

    assert order_item.product_id == product.id
    assert order_item.variant_id is None
    assert order_item.product_name == product.name
    assert order_item.quantity == 2
    assert order_item.unit_price == product.price
    assert order_item.total_price == product.price * 2


def test_create_order_decreases_product_stock(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    original_stock = product.stock_quantity

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=3,
    )

    service.create_order(authenticated_user.id)

    db_session.refresh(product)

    assert product.stock_quantity == original_stock - 3


def test_create_order_clears_cart(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=2,
    )

    service.create_order(authenticated_user.id)

    remaining_items = (
        db_session.query(CartItem)
        .filter(CartItem.cart_id == cart.id)
        .all()
    )

    assert remaining_items == []


# -------------------------
# Multiple items
# -------------------------


def test_create_order_with_multiple_items(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    second_product = product.__class__(
        sub_category_id=product.sub_category_id,
        name="Another Shirt",
        slug="another-shirt",
        description="Another shirt",
        price=3000,
        currency="USD",
        stock_quantity=10,
        image_url="https://example.com/images/another-shirt.jpg",
        is_active=True,
    )

    db_session.add(second_product)
    db_session.commit()
    db_session.refresh(second_product)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=2,
    )

    create_cart_item(
        db_session,
        cart,
        second_product,
        quantity=1,
    )

    order = service.create_order(authenticated_user.id)

    expected_subtotal = (
        product.price * 2
        + second_product.price
    )

    assert order.subtotal == expected_subtotal
    assert order.total == expected_subtotal
    assert len(order.items) == 2


# -------------------------
# Variant checkout
# -------------------------


def create_variant(
    db_session,
    product,
    sku="CLASSIC-M-BLACK",
    size="M",
    color="Black",
    price=2999,
    stock_quantity=10,
):

    variant = ProductVariant(
        product_id=product.id,
        sku=sku,
        size=size,
        color=color,
        material=None,
        price=price,
        stock_quantity=stock_quantity,
        is_active=True,
    )

    db_session.add(variant)
    db_session.commit()
    db_session.refresh(variant)

    return variant


def test_create_order_with_variant(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    variant = create_variant(
        db_session,
        product,
    )

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=2,
        variant=variant,
    )

    order = service.create_order(authenticated_user.id)

    assert len(order.items) == 1

    order_item = order.items[0]

    assert order_item.product_id == product.id
    assert order_item.variant_id == variant.id
    assert order_item.product_name == product.name
    assert order_item.sku == variant.sku
    assert order_item.quantity == 2
    assert order_item.unit_price == variant.price
    assert order_item.total_price == variant.price * 2

    assert order.subtotal == variant.price * 2


def test_create_order_decreases_variant_stock(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    variant = create_variant(
        db_session,
        product,
        stock_quantity=10,
    )

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=4,
        variant=variant,
    )

    service.create_order(authenticated_user.id)

    db_session.refresh(variant)

    assert variant.stock_quantity == 6


# -------------------------
# Price snapshot
# -------------------------


def test_order_snapshots_product_price(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    original_price = product.price

    order = service.create_order(authenticated_user.id)

    order_item = order.items[0]

    assert order_item.unit_price == original_price


def test_order_snapshots_variant_price(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    variant = create_variant(
        db_session,
        product,
        price=3499,
    )

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
        variant=variant,
    )

    original_price = variant.price

    order = service.create_order(authenticated_user.id)

    order_item = order.items[0]

    assert order_item.unit_price == original_price


# -------------------------
# Cart validation
# -------------------------


def test_create_order_without_cart_raises_error(
    db_session,
    authenticated_user,
):
    service = create_order_service(db_session)

    with pytest.raises(CartNotFoundError):
        service.create_order(authenticated_user.id)


def test_create_order_with_empty_cart_raises_error(
    db_session,
    authenticated_user,
):
    service = create_order_service(db_session)

    create_cart(
        db_session,
        authenticated_user,
    )

    with pytest.raises(CartEmptyError):
        service.create_order(authenticated_user.id)


# -------------------------
# Product validation
# -------------------------


def test_create_order_with_inactive_product(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    product.is_active = False
    db_session.commit()

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    with pytest.raises(ProductNotFoundError):
        service.create_order(authenticated_user.id)


# -------------------------
# Stock validation
# -------------------------


def test_create_order_with_product_out_of_stock(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    product.stock_quantity = 0
    db_session.commit()

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    with pytest.raises(ProductOutOfStockError):
        service.create_order(authenticated_user.id)


def test_create_order_with_insufficient_product_stock(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    product.stock_quantity = 2
    db_session.commit()

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=3,
    )

    with pytest.raises(InsufficientStockError):
        service.create_order(authenticated_user.id)


# -------------------------
# Variant validation
# -------------------------


def test_create_order_with_inactive_variant(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    variant = create_variant(
        db_session,
        product,
    )

    variant.is_active = False
    db_session.commit()

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
        variant=variant,
    )

    with pytest.raises(ProductVariantNotFoundError):
        service.create_order(authenticated_user.id)
    

def test_create_order_with_variant_out_of_stock(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    variant = create_variant(
        db_session,
        product,
        stock_quantity=0,
    )

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
        variant=variant,
    )

    with pytest.raises(ProductOutOfStockError):
        service.create_order(authenticated_user.id)


def test_create_order_with_insufficient_variant_stock(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    service = create_order_service(db_session)

    variant = create_variant(
        db_session,
        product,
        stock_quantity=2,
    )

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=3,
        variant=variant,
    )

    with pytest.raises(InsufficientStockError):
        service.create_order(authenticated_user.id)


def test_create_order_with_nonexistent_variant(
    db_session,
    authenticated_user,
    monkeypatch,
):
    product = create_product(db_session)
    variant = create_variant(
        db_session,
        product,
        sku="NONEXISTENT-VARIANT-TEST",
    )

    service = create_order_service(db_session)

    cart = create_cart(
        db_session,
        authenticated_user,
    )

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
        variant=variant,
    )

    def return_none(*args, **kwargs):
        return None

    monkeypatch.setattr(
        service.product_variant_repository,
        "get_by_id",
        return_none,
    )

    with pytest.raises(ProductVariantNotFoundError):
        service.create_order(authenticated_user.id)


def test_create_order_with_variant_from_different_product(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    second_product = Product(
        sub_category_id=product.sub_category_id,
        name="Another Shirt",
        slug="another-shirt",
        description="Another shirt",
        price=3000,
        currency="USD",
        stock_quantity=10,
        image_url="https://example.com/images/another-shirt.jpg",
        is_active=True,
    )

    db_session.add(second_product)
    db_session.commit()
    db_session.refresh(second_product)

    variant = create_variant(
        db_session,
        second_product,
    )

    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    cart_item = create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    cart_item.variant_id = variant.id
    db_session.commit()

    with pytest.raises(ProductVariantNotFoundError):
        service.create_order(authenticated_user.id)


def test_order_status_lifecycle(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    order = service.create_order(authenticated_user.id)

    order = service.update_order_status(
        order.id,
        OrderStatus.CONFIRMED,
    )
    assert order.status == OrderStatus.CONFIRMED

    order = service.update_order_status(
        order.id,
        OrderStatus.PROCESSING,
    )
    assert order.status == OrderStatus.PROCESSING

    order = service.update_order_status(
        order.id,
        OrderStatus.SHIPPED,
    )
    assert order.status == OrderStatus.SHIPPED

    order = service.update_order_status(
        order.id,
        OrderStatus.DELIVERED,
    )
    assert order.status == OrderStatus.DELIVERED


def test_cannot_move_delivered_order(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    order = service.create_order(authenticated_user.id)

    service.update_order_status(order.id, OrderStatus.CONFIRMED)
    service.update_order_status(order.id, OrderStatus.PROCESSING)
    service.update_order_status(order.id, OrderStatus.SHIPPED)
    service.update_order_status(order.id, OrderStatus.DELIVERED)

    with pytest.raises(InvalidOrderStatusTransitionError):
        service.update_order_status(
            order.id,
            OrderStatus.CANCELLED,
        )


def test_cancel_pending_order(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    order = service.create_order(authenticated_user.id)

    cancelled_order = service.cancel_order(
        order.id,
        authenticated_user.id,
    )

    assert cancelled_order.status == OrderStatus.CANCELLED


def test_cancel_confirmed_order(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    order = service.create_order(authenticated_user.id)

    service.update_order_status(
        order.id,
        OrderStatus.CONFIRMED,
    )

    cancelled_order = service.cancel_order(
        order.id,
        authenticated_user.id,
    )

    assert cancelled_order.status == OrderStatus.CANCELLED


def test_cannot_cancel_processing_order(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    order = service.create_order(authenticated_user.id)

    service.update_order_status(
        order.id,
        OrderStatus.CONFIRMED,
    )

    service.update_order_status(
        order.id,
        OrderStatus.PROCESSING,
    )

    with pytest.raises(InvalidOrderStatusTransitionError):
        service.cancel_order(
            order.id,
            authenticated_user.id,
        )


def test_get_nonexistent_order_raises_error(
    db_session,
    authenticated_user,
):
    service = create_order_service(db_session)

    with pytest.raises(OrderNotFoundError):
        service.get_order(
            uuid4(),
            authenticated_user.id,
        )


def test_user_cannot_access_another_users_order(
    db_session,
    authenticated_user,
):
    another_user = User(
        first_name="Another",
        last_name="User",
        mobile="5555555555",
        email="another@example.com",
        password="hashed-password",
        date_of_birth=date(1996, 1, 1),
        role=UserRole.CUSTOMER,
        is_verified=True,
    )

    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)

    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(
        db_session,
        authenticated_user,
    )

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=1,
    )

    order = service.create_order(
        authenticated_user.id,
    )

    with pytest.raises(OrderNotFoundError):
        service.get_order(
            order.id,
            another_user.id,
        )


def test_user_cannot_cancel_another_users_order(
    db_session,
    authenticated_user,
):
    another_user = User(
        first_name="Another",
        last_name="User",
        mobile="5555555555",
        email="another@example.com",
        password="hashed-password",
        date_of_birth=date(1996, 1, 1),
        role=UserRole.CUSTOMER,
        is_verified=True,
    )

    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)

    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)
    create_cart_item(db_session, cart, product)

    order = service.create_order(authenticated_user.id)

    with pytest.raises(OrderNotFoundError):
        service.cancel_order(
            order.id,
            another_user.id,
        )


def test_cannot_skip_order_status(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)
    create_cart_item(db_session, cart, product)

    order = service.create_order(authenticated_user.id)

    with pytest.raises(InvalidOrderStatusTransitionError):
        service.update_order_status(
            order.id,
            OrderStatus.SHIPPED,
        )


def test_cannot_update_delivered_order(
    db_session,
    authenticated_user,
):
    product = create_product(db_session)
    service = create_order_service(db_session)

    cart = create_cart(db_session, authenticated_user)
    create_cart_item(db_session, cart, product)

    order = service.create_order(authenticated_user.id)

    service.update_order_status(order.id, OrderStatus.CONFIRMED)
    service.update_order_status(order.id, OrderStatus.PROCESSING)
    service.update_order_status(order.id, OrderStatus.SHIPPED)
    service.update_order_status(order.id, OrderStatus.DELIVERED)

    with pytest.raises(InvalidOrderStatusTransitionError):
        service.update_order_status(
            order.id,
            OrderStatus.CONFIRMED,
        )


def test_update_nonexistent_order_raises_error(
    db_session,
    authenticated_user,
):
    service = create_order_service(db_session)

    with pytest.raises(OrderNotFoundError):
        service.update_order_status(
            uuid4(),
            OrderStatus.CONFIRMED,
        )


def test_cancel_nonexistent_order_raises_error(
    db_session,
    authenticated_user,
):
    service = create_order_service(db_session)

    with pytest.raises(OrderNotFoundError):
        service.cancel_order(
            uuid4(),
            authenticated_user.id,
        )


def test_create_order_rolls_back_on_failure(
    db_session,
    authenticated_user,
):
    product_one = create_product(db_session)

    category = Category(
        name="Women",
        slug="women",
        description="Women's clothing",
        image_url="https://example.com/images/women.jpg",
        is_active=True,
    )

    db_session.add(category)
    db_session.flush()

    sub_category = SubCategory(
        category_id=category.id,
        name="Dresses",
        slug="dresses",
        description="Women's dresses",
        image_url="https://example.com/images/dresses.jpg",
        is_active=True,
    )

    db_session.add(sub_category)
    db_session.flush()

    product_two = Product(
        sub_category_id=sub_category.id,
        name="Limited Dress",
        slug="limited-dress",
        description="Limited stock dress",
        price=4999,
        currency="USD",
        stock_quantity=1,
        image_url="https://example.com/images/dress.jpg",
        is_active=True,
    )

    db_session.add(product_two)
    db_session.commit()
    db_session.refresh(product_two)

    service = create_order_service(db_session)

    cart = create_cart(
        db_session,
        authenticated_user,
    )

    create_cart_item(
        db_session,
        cart,
        product_one,
        quantity=1,
    )

    create_cart_item(
        db_session,
        cart,
        product_two,
        quantity=2,
    )

    with pytest.raises(InsufficientStockError):
        service.create_order(authenticated_user.id)

    db_session.expire_all()

    refreshed_product_one = (
        db_session.query(Product)
        .filter(Product.id == product_one.id)
        .one()
    )

    refreshed_product_two = (
        db_session.query(Product)
        .filter(Product.id == product_two.id)
        .one()
    )

    assert refreshed_product_one.stock_quantity == 25
    assert refreshed_product_two.stock_quantity == 1

    orders = (
        db_session.query(Order)
        .filter(Order.user_id == authenticated_user.id)
        .all()
    )

    assert orders == []

    cart_items = (
        db_session.query(CartItem)
        .filter(CartItem.cart_id == cart.id)
        .all()
    )

    assert len(cart_items) == 2


def create_order(
    db_session,
    user,
    product,
    status=OrderStatus.PENDING,
):
    order = Order(
        user_id=user.id,
        status=status,
        subtotal=product.price,
        tax=0,
        shipping_cost=0,
        total=product.price,
        currency="USD",
    )

    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    return order


# ---------------------------------------------------------------------------
# CREATE ORDER
# ---------------------------------------------------------------------------


def test_create_order_success(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)
    cart = create_cart(db_session, authenticated_user)

    create_cart_item(
        db_session,
        cart,
        product,
        quantity=2,
    )

    response = customer_client.post("/orders")

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] == str(authenticated_user.id)
    assert data["status"] == "pending"
    assert data["subtotal"] == product.price * 2
    assert data["total"] == product.price * 2
    assert len(data["items"]) == 1

    assert data["items"][0]["product_id"] == str(product.id)
    assert data["items"][0]["quantity"] == 2


def test_create_order_requires_authentication(client):
    response = client.post("/orders")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET ORDERS
# ---------------------------------------------------------------------------


def test_get_orders_returns_user_orders(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    first_order = create_order(
        db_session,
        authenticated_user,
        product,
    )

    second_order = create_order(
        db_session,
        authenticated_user,
        product,
    )

    response = customer_client.get("/orders")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    returned_ids = {item["id"] for item in data}

    assert str(first_order.id) in returned_ids
    assert str(second_order.id) in returned_ids


def test_get_orders_requires_authentication(client):
    response = client.get("/orders")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET SINGLE ORDER
# ---------------------------------------------------------------------------


def test_get_order_success(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    order = create_order(
        db_session,
        authenticated_user,
        product,
    )

    response = customer_client.get(
        f"/orders/{order.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(order.id)
    assert data["user_id"] == str(authenticated_user.id)
    assert data["status"] == "pending"


def test_get_order_not_found(
    customer_client,
):
    order_id = uuid4()

    response = customer_client.get(
        f"/orders/{order_id}"
    )

    assert response.status_code == 404


def test_user_cannot_access_another_users_order(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    another_user = User(
        first_name="Another",
        last_name="User",
        mobile="5555555555",
        email="another@example.com",
        password="hashed-password",
        date_of_birth="1995-01-01",
        role=UserRole.CUSTOMER,
        is_verified=True,
    )

    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)

    order = create_order(
        db_session,
        another_user,
        product,
    )

    response = customer_client.get(
        f"/orders/{order.id}"
    )

    assert response.status_code == 404


def test_get_order_requires_authentication(client):
    response = client.get(
        f"/orders/{uuid4()}"
    )

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# CANCEL ORDER
# ---------------------------------------------------------------------------


def test_cancel_pending_order(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    order = create_order(
        db_session,
        authenticated_user,
        product,
        status=OrderStatus.PENDING,
    )

    response = customer_client.post(
        f"/orders/{order.id}/cancel"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(order.id)
    assert data["status"] == "cancelled"


def test_cancel_confirmed_order(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    order = create_order(
        db_session,
        authenticated_user,
        product,
        status=OrderStatus.CONFIRMED,
    )

    response = customer_client.post(
        f"/orders/{order.id}/cancel"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "cancelled"


def test_cancel_processing_order_returns_conflict(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    order = create_order(
        db_session,
        authenticated_user,
        product,
        status=OrderStatus.PROCESSING,
    )

    response = customer_client.post(
        f"/orders/{order.id}/cancel"
    )

    assert response.status_code == 409


def test_user_cannot_cancel_another_users_order(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    another_user = User(
        first_name="Another",
        last_name="User",
        mobile="5555555555",
        email="another@example.com",
        password="hashed-password",
        date_of_birth="1995-01-01",
        role=UserRole.CUSTOMER,
        is_verified=True,
    )

    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)

    order = create_order(
        db_session,
        another_user,
        product,
    )

    response = customer_client.post(
        f"/orders/{order.id}/cancel"
    )

    assert response.status_code == 404


def test_cancel_order_requires_authentication(client):
    response = client.post(
        f"/orders/{uuid4()}/cancel"
    )

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# ADMIN STATUS UPDATE
# ---------------------------------------------------------------------------


def test_admin_can_update_order_status(
    admin_client,
    db_session,
    admin_user,
):
    product = create_product(db_session)

    order = create_order(
        db_session,
        admin_user,
        product,
        status=OrderStatus.PENDING,
    )

    response = admin_client.patch(
        f"/orders/{order.id}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(order.id)
    assert data["status"] == "confirmed"


def test_customer_cannot_update_order_status(
    customer_client,
    db_session,
    authenticated_user,
):
    product = create_product(db_session)

    order = create_order(
        db_session,
        authenticated_user,
        product,
    )

    response = customer_client.patch(
        f"/orders/{order.id}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 403

    assert response.json()["detail"] == "Admin access required"


def test_unauthenticated_user_cannot_update_order_status(
    client,
):
    response = client.patch(
        f"/orders/{uuid4()}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 401


def test_admin_cannot_skip_order_status(
    admin_client,
    db_session,
    admin_user,
):
    product = create_product(db_session)

    order = create_order(
        db_session,
        admin_user,
        product,
        status=OrderStatus.PENDING,
    )

    response = admin_client.patch(
        f"/orders/{order.id}/status",
        json={"status": "shipped"},
    )

    assert response.status_code == 409


def test_admin_update_nonexistent_order_returns_not_found(
    admin_client,
):
    response = admin_client.patch(
        f"/orders/{uuid4()}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 404
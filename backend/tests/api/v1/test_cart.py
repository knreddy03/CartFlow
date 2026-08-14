from uuid import uuid4
from datetime import date

from app.models.category import Category
from app.models.product import Product

from app.dependencies.user import get_current_user_id
from app.main import app
from app.models.user import User


def create_category(db_session):
    category = Category(
        name="Men",
        slug="men",
        description="Men's clothing",
        image_url="https://example.com/images/men.jpg",
        is_active=True,
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    return category


def create_product(
    db_session,
    category,
    *,
    name="Men's Shirt",
    slug="mens-shirt",
    price=1999,
    stock_quantity=10,
    is_active=True,
):
    product = Product(
        category_id=category.id,
        name=name,
        slug=slug,
        description="Men's clothing",
        price=price,
        currency="USD",
        stock_quantity=stock_quantity,
        image_url="https://example.com/images/shirt.jpg",
        is_active=is_active,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product


def test_get_cart(authenticated_client):
    response = authenticated_client.get("/cart")

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "user_id" in data
    assert "items" in data
    assert data["items"] == []
    assert "created_at" in data
    assert "updated_at" in data


def test_add_item_to_cart(authenticated_client, db_session):
    category = create_category(db_session)
    product = create_product(db_session, category)

    response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["product_id"] == str(product.id)
    assert data["quantity"] == 2
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_add_same_product_increases_quantity(authenticated_client, db_session):
    category = create_category(db_session)
    product = create_product(db_session, category)

    first_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 2,
        },
    )

    assert first_response.status_code == 201

    second_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 3,
        },
    )

    assert second_response.status_code == 201

    data = second_response.json()

    assert data["product_id"] == str(product.id)
    assert data["quantity"] == 5


def test_update_cart_item(authenticated_client, db_session):
    category = create_category(db_session)
    product = create_product(db_session, category)

    create_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 2,
        },
    )

    assert create_response.status_code == 201

    cart_item_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/cart/items/{cart_item_id}",
        json={
            "quantity": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == cart_item_id
    assert data["product_id"] == str(product.id)
    assert data["quantity"] == 5


def test_delete_cart_item(authenticated_client, db_session):
    category = create_category(db_session)
    product = create_product(db_session, category)

    create_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 2,
        },
    )

    assert create_response.status_code == 201

    cart_item_id = create_response.json()["id"]

    response = authenticated_client.delete(
        f"/cart/items/{cart_item_id}"
    )

    assert response.status_code == 204

    cart_response = authenticated_client.get("/cart")

    assert cart_response.status_code == 200
    assert cart_response.json()["items"] == []


def test_add_nonexistent_product(authenticated_client):
    response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(uuid4()),
            "quantity": 1,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."


def test_update_cart_item_not_found(authenticated_client):
    response = authenticated_client.patch(
        f"/cart/items/{uuid4()}",
        json={
            "quantity": 2,
        },
    )

    assert response.status_code == 404


def test_delete_cart_item_not_found(authenticated_client):
    response = authenticated_client.delete(
        f"/cart/items/{uuid4()}"
    )

    assert response.status_code == 404


def test_add_out_of_stock_product(authenticated_client, db_session):
    category = create_category(db_session)

    product = create_product(
        db_session,
        category,
        stock_quantity=0,
    )

    response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 1,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Product is out of stock."


def test_add_quantity_exceeds_stock(authenticated_client, db_session):
    category = create_category(db_session)

    product = create_product(
        db_session,
        category,
        stock_quantity=5,
    )

    response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 6,
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "Requested quantity exceeds available stock."
    )


def test_add_existing_quantity_exceeds_stock(
    authenticated_client,
    db_session,
):
    category = create_category(db_session)

    product = create_product(
        db_session,
        category,
        stock_quantity=5,
    )

    first_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 3,
        },
    )

    assert first_response.status_code == 201

    second_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 3,
        },
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"]
        == "Requested quantity exceeds available stock."
    )


def test_add_inactive_product(authenticated_client, db_session):
    category = create_category(db_session)

    product = create_product(
        db_session,
        category,
        is_active=False,
        stock_quantity=10,
    )

    response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 1,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."


def test_update_quantity_exceeds_stock(
    authenticated_client,
    db_session,
):
    category = create_category(db_session)

    product = create_product(
        db_session,
        category,
        stock_quantity=5,
    )

    create_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 2,
        },
    )

    assert create_response.status_code == 201

    cart_item_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/cart/items/{cart_item_id}",
        json={
            "quantity": 6,
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "Requested quantity exceeds available stock."
    )


def test_user_cannot_modify_another_users_cart_item(
    authenticated_client,
    authenticated_user,
    db_session,
):
    category = create_category(db_session)
    product = create_product(db_session, category)

    # User A adds the product to their cart.
    create_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 2,
        },
    )

    assert create_response.status_code == 201

    cart_item_id = create_response.json()["id"]

    # Create User B.
    user_b = User(
        first_name="Another",
        last_name="User",
        mobile="1234567891",
        email="another@example.com",
        password="hashed-password",
        date_of_birth=date(1995, 1, 1),
        is_verified=True,
    )

    db_session.add(user_b)
    db_session.commit()
    db_session.refresh(user_b)

    # Authenticate as User B.
    def override_user_b():
        return user_b.id

    app.dependency_overrides[get_current_user_id] = override_user_b

    try:
        response = authenticated_client.patch(
            f"/cart/items/{cart_item_id}",
            json={
                "quantity": 5,
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Cart not found."

    finally:
        app.dependency_overrides[get_current_user_id] = (
            lambda: authenticated_user.id
        )


def test_user_cannot_delete_another_users_cart_item(
    authenticated_client,
    authenticated_user,
    db_session,
):
    category = create_category(db_session)
    product = create_product(db_session, category)

    create_response = authenticated_client.post(
        "/cart/items",
        json={
            "product_id": str(product.id),
            "quantity": 2,
        },
    )

    assert create_response.status_code == 201

    cart_item_id = create_response.json()["id"]

    user_b = User(
        first_name="Another",
        last_name="User",
        mobile="1234567891",
        email="another@example.com",
        password="hashed-password",
        date_of_birth=date(1995, 1, 1),
        is_verified=True,
    )

    db_session.add(user_b)
    db_session.commit()
    db_session.refresh(user_b)

    def override_user_b():
        return user_b.id

    app.dependency_overrides[get_current_user_id] = override_user_b

    try:
        response = authenticated_client.delete(
            f"/cart/items/{cart_item_id}"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Cart not found."

    finally:
        app.dependency_overrides[get_current_user_id] = (
            lambda: authenticated_user.id
        )
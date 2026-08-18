from uuid import uuid4

from app.models.category import Category
from app.models.product import Product
from app.models.sub_category import SubCategory


def create_category_and_sub_category(
    db_session,
    category_name="Men",
    category_slug="men",
    sub_category_name="Shirts",
    sub_category_slug="shirts",
):
    category = Category(
        name=category_name,
        slug=category_slug,
        description=f"{category_name} clothing",
        image_url=f"https://example.com/images/{category_slug}.jpg",
        is_active=True,
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    sub_category = SubCategory(
        category_id=category.id,
        name=sub_category_name,
        slug=sub_category_slug,
        description=f"{sub_category_name} for {category_name}",
        image_url=f"https://example.com/images/{sub_category_slug}.jpg",
        is_active=True,
    )

    db_session.add(sub_category)
    db_session.commit()
    db_session.refresh(sub_category)

    return category, sub_category


def test_create_product(client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    response = client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category.id),
            "name": "Men's Shirt",
            "slug": "mens-shirt",
            "description": "Men's clothing and accessories",
            "price": 1999,
            "currency": "USD",
            "stock_quantity": 25,
            "image_url": "https://example.com/images/mens-shirt.jpg",
            "is_active": True,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Men's Shirt"
    assert data["slug"] == "mens-shirt"
    assert data["description"] == "Men's clothing and accessories"
    assert data["price"] == 1999
    assert data["currency"] == "USD"
    assert data["stock_quantity"] == 25
    assert data["sub_category_id"] == str(sub_category.id)
    assert data["image_url"] == "https://example.com/images/mens-shirt.jpg"
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

    product = db_session.get(Product, data["id"])

    assert product is not None
    assert product.sub_category_id == sub_category.id
    assert product.name == "Men's Shirt"
    assert product.slug == "mens-shirt"
    assert product.price == 1999
    assert product.currency == "USD"
    assert product.stock_quantity == 25


def test_get_products(client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Women",
        category_slug="women",
        sub_category_name="Dresses",
        sub_category_slug="dresses",
    )

    create_response = client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category.id),
            "name": "Women's Dress",
            "slug": "womens-dress",
            "description": "Women's summer dress",
            "price": 2999,
            "currency": "USD",
            "stock_quantity": 15,
            "image_url": "https://example.com/images/dress.jpg",
            "is_active": True,
        },
    )

    assert create_response.status_code == 201

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    product = data[0]

    assert product["sub_category_id"] == str(sub_category.id)
    assert product["name"] == "Women's Dress"
    assert product["slug"] == "womens-dress"
    assert product["description"] == "Women's summer dress"
    assert product["price"] == 2999
    assert product["currency"] == "USD"
    assert product["stock_quantity"] == 15
    assert product["image_url"] == "https://example.com/images/dress.jpg"
    assert product["is_active"] is True


def test_get_product_by_id(client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Kids",
        category_slug="kids",
        sub_category_name="T-Shirts",
        sub_category_slug="t-shirts",
    )

    create_response = client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category.id),
            "name": "Kids T-Shirt",
            "slug": "kids-t-shirt",
            "description": "Kids cotton t-shirt",
            "price": 1499,
            "currency": "USD",
            "stock_quantity": 20,
            "image_url": "https://example.com/images/kids-tshirt.jpg",
            "is_active": True,
        },
    )

    assert create_response.status_code == 201

    created_product = create_response.json()
    product_id = created_product["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["sub_category_id"] == str(sub_category.id)
    assert data["name"] == "Kids T-Shirt"
    assert data["slug"] == "kids-t-shirt"
    assert data["description"] == "Kids cotton t-shirt"
    assert data["price"] == 1499
    assert data["currency"] == "USD"
    assert data["stock_quantity"] == 20
    assert data["image_url"] == "https://example.com/images/kids-tshirt.jpg"
    assert data["is_active"] is True


def test_get_product_not_found(client):
    product_id = uuid4()

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."


def test_update_product(client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    create_response = client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category.id),
            "name": "Men's Shirt",
            "slug": "mens-shirt",
            "description": "Men's clothing",
            "price": 1999,
            "currency": "USD",
            "stock_quantity": 25,
            "image_url": "https://example.com/images/mens-shirt.jpg",
            "is_active": True,
        },
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = client.patch(
        f"/products/{product_id}",
        json={
            "name": "Men's Premium Shirt",
            "description": "Premium men's shirt",
            "price": 2499,
            "stock_quantity": 40,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["sub_category_id"] == str(sub_category.id)
    assert data["name"] == "Men's Premium Shirt"
    assert data["slug"] == "mens-shirt"
    assert data["description"] == "Premium men's shirt"
    assert data["price"] == 2499
    assert data["currency"] == "USD"
    assert data["stock_quantity"] == 40
    assert data["image_url"] == "https://example.com/images/mens-shirt.jpg"
    assert data["is_active"] is True


def test_create_duplicate_product(client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Women",
        category_slug="women",
        sub_category_name="Dresses",
        sub_category_slug="dresses",
    )

    product_data = {
        "sub_category_id": str(sub_category.id),
        "name": "Women's Dress",
        "slug": "womens-dress",
        "description": "Women's summer dress",
        "price": 2999,
        "currency": "USD",
        "stock_quantity": 15,
        "image_url": "https://example.com/images/women.jpg",
        "is_active": True,
    }

    first_response = client.post(
        "/products",
        json=product_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/products",
        json=product_data,
    )

    assert second_response.status_code == 409


def test_update_product_not_found(client):
    product_id = uuid4()

    response = client.patch(
        f"/products/{product_id}",
        json={
            "name": "Updated Product",
        },
    )

    assert response.status_code == 404


def test_delete_product(client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Kids",
        category_slug="kids",
        sub_category_name="T-Shirts",
        sub_category_slug="t-shirts",
    )

    create_response = client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category.id),
            "name": "Kids T-Shirt",
            "slug": "kids-t-shirt",
            "description": "Kids cotton t-shirt",
            "price": 2999,
            "currency": "USD",
            "stock_quantity": 10,
            "image_url": "https://example.com/images/kids-tshirt.jpg",
            "is_active": True,
        },
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/products/{product_id}"
    )

    assert get_response.status_code == 404


def test_delete_product_not_found(client):
    product_id = uuid4()

    response = client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 404
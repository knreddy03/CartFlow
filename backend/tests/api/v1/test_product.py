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


def create_product(
    admin_client,
    sub_category_id,
    name,
    slug,
    price=1999,
    stock_quantity=25,
    is_active=True,
):
    return admin_client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category_id),
            "name": name,
            "slug": slug,
            "description": f"{name} description",
            "price": price,
            "currency": "USD",
            "stock_quantity": stock_quantity,
            "image_url": f"https://example.com/images/{slug}.jpg",
            "is_active": is_active,
        },
    )


def test_create_product(admin_client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    response = admin_client.post(
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


def test_get_products(admin_client, client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Women",
        category_slug="women",
        sub_category_name="Dresses",
        sub_category_slug="dresses",
    )

    create_response = create_product(
        admin_client,
        sub_category.id,
        "Women's Dress",
        "womens-dress",
        price=2999,
        stock_quantity=15,
    )

    assert create_response.status_code == 201

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] == 1
    assert len(data["items"]) == 1

    product = data["items"][0]

    assert product["sub_category_id"] == str(sub_category.id)
    assert product["name"] == "Women's Dress"
    assert product["slug"] == "womens-dress"
    assert product["description"] == "Women's Dress description"
    assert product["price"] == 2999
    assert product["currency"] == "USD"
    assert product["stock_quantity"] == 15
    assert product["image_url"] == (
        "https://example.com/images/womens-dress.jpg"
    )
    assert product["is_active"] is True


def test_get_products_filter_by_category(admin_client, client, db_session):
    category, shirts = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    pants = SubCategory(
        category_id=category.id,
        name="Pants",
        slug="pants",
        description="Pants for Men",
        image_url="https://example.com/images/pants.jpg",
        is_active=True,
    )

    db_session.add(pants)
    db_session.commit()
    db_session.refresh(pants)

    shirt_response = create_product(
        admin_client,
        shirts.id,
        "Men's Shirt",
        "mens-shirt",
    )

    pants_response = create_product(
        admin_client,
        pants.id,
        "Men's Pants",
        "mens-pants",
    )

    assert shirt_response.status_code == 201
    assert pants_response.status_code == 201

    response = client.get(
        f"/products?category_id={category.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2

    product_names = {
        product["name"]
        for product in data["items"]
    }

    assert product_names == {
        "Men's Shirt",
        "Men's Pants",
    }


def test_get_products_filter_by_sub_category(admin_client, client, db_session):
    _, shirts = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    _, pants = create_category_and_sub_category(
        db_session,
        category_name="Women",
        category_slug="women",
        sub_category_name="Pants",
        sub_category_slug="pants",
    )

    assert create_product(
        admin_client,
        shirts.id,
        "Men's Shirt",
        "mens-shirt",
    ).status_code == 201

    assert create_product(
        admin_client,
        pants.id,
        "Women's Pants",
        "womens-pants",
    ).status_code == 201

    response = client.get(
        f"/products?sub_category_id={shirts.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Men's Shirt"
    assert data["items"][0]["sub_category_id"] == str(shirts.id)


def test_get_products_filter_by_active_status(admin_client, client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    assert create_product(
        admin_client,
        sub_category.id,
        "Active Shirt",
        "active-shirt",
        is_active=True,
    ).status_code == 201

    assert create_product(
        admin_client,
        sub_category.id,
        "Inactive Shirt",
        "inactive-shirt",
        is_active=False,
    ).status_code == 201

    response = client.get("/products?is_active=true")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Active Shirt"
    assert data["items"][0]["is_active"] is True


def test_get_products_filter_by_min_price(admin_client, client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    assert create_product(
        admin_client,
        sub_category.id,
        "Cheap Shirt",
        "cheap-shirt",
        price=1500,
    ).status_code == 201

    assert create_product(
        admin_client,
        sub_category.id,
        "Expensive Shirt",
        "expensive-shirt",
        price=3000,
    ).status_code == 201

    response = client.get("/products?min_price=2500")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Expensive Shirt"


def test_get_products_filter_by_max_price(admin_client, client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    assert create_product(
        admin_client,
        sub_category.id,
        "Cheap Shirt",
        "cheap-shirt",
        price=1500,
    ).status_code == 201

    assert create_product(
        admin_client,
        sub_category.id,
        "Expensive Shirt",
        "expensive-shirt",
        price=3000,
    ).status_code == 201

    response = client.get("/products?max_price=2000")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Cheap Shirt"


def test_get_products_filter_by_price_range(admin_client, client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    assert create_product(
        admin_client,
        sub_category.id,
        "Cheap Shirt",
        "cheap-shirt",
        price=1000,
    ).status_code == 201

    assert create_product(
        admin_client,
        sub_category.id,
        "Medium Shirt",
        "medium-shirt",
        price=2000,
    ).status_code == 201

    assert create_product(
        admin_client,
        sub_category.id,
        "Expensive Shirt",
        "expensive-shirt",
        price=4000,
    ).status_code == 201

    response = client.get(
        "/products?min_price=1500&max_price=2500"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Medium Shirt"


def test_get_products_with_combined_filters(admin_client, client, db_session):
    _, shirts = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    _, pants = create_category_and_sub_category(
        db_session,
        category_name="Women",
        category_slug="women",
        sub_category_name="Pants",
        sub_category_slug="pants",
    )

    assert create_product(
        admin_client,
        shirts.id,
        "Active Shirt",
        "active-shirt",
        price=2500,
        is_active=True,
    ).status_code == 201

    assert create_product(
        admin_client,
        shirts.id,
        "Inactive Shirt",
        "inactive-shirt",
        price=2500,
        is_active=False,
    ).status_code == 201

    assert create_product(
        admin_client,
        pants.id,
        "Active Pants",
        "active-pants",
        price=2500,
        is_active=True,
    ).status_code == 201

    response = client.get(
        f"/products?"
        f"sub_category_id={shirts.id}"
        f"&is_active=true"
        f"&min_price=2000"
        f"&max_price=3000"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Active Shirt"


def test_get_products_pagination(admin_client, client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    products = [
        ("Shirt A", "shirt-a"),
        ("Shirt B", "shirt-b"),
        ("Shirt C", "shirt-c"),
        ("Shirt D", "shirt-d"),
        ("Shirt E", "shirt-e"),
    ]

    for name, slug in products:
        response = create_product(
            admin_client,
            sub_category.id,
            name,
            slug,
        )

        assert response.status_code == 201

    response = client.get(
        "/products?page=1&page_size=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total_pages"] == 3
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "Shirt A"
    assert data["items"][1]["name"] == "Shirt B"


def test_get_products_second_page(admin_client, client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    products = [
        ("Shirt A", "shirt-a"),
        ("Shirt B", "shirt-b"),
        ("Shirt C", "shirt-c"),
        ("Shirt D", "shirt-d"),
        ("Shirt E", "shirt-e"),
    ]

    for name, slug in products:
        response = create_product(
            admin_client,
            sub_category.id,
            name,
            slug,
        )

        assert response.status_code == 201

    response = client.get(
        "/products?page=2&page_size=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 5
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert data["total_pages"] == 3
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "Shirt C"
    assert data["items"][1]["name"] == "Shirt D"


def test_get_products_empty_result(admin_client, client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    response = client.get(
        f"/products?sub_category_id={sub_category.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] == 0


def test_get_products_invalid_page(client):
    response = client.get("/products?page=0")

    assert response.status_code == 422


def test_get_products_invalid_page_size(client):
    response = client.get("/products?page_size=0")

    assert response.status_code == 422


def test_get_products_page_size_too_large(client):
    response = client.get("/products?page_size=101")

    assert response.status_code == 422


def test_get_products_negative_min_price(client):
    response = client.get("/products?min_price=-1")

    assert response.status_code == 422


def test_get_products_negative_max_price(client):
    response = client.get("/products?max_price=-1")

    assert response.status_code == 422


def test_get_products_min_price_greater_than_max_price(client):
    response = client.get(
        "/products?min_price=5000&max_price=2000"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "min_price cannot be greater than max_price."
    )


def test_get_products_invalid_sub_category(client):
    sub_category_id = uuid4()

    response = client.get(
        f"/products?sub_category_id={sub_category_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sub Category not found."


def test_get_product_by_id(admin_client, client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Kids",
        category_slug="kids",
        sub_category_name="T-Shirts",
        sub_category_slug="t-shirts",
    )

    create_response = create_product(
        admin_client,
        sub_category.id,
        "Kids T-Shirt",
        "kids-t-shirt",
        price=1499,
        stock_quantity=20,
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
    assert data["price"] == 1499
    assert data["currency"] == "USD"
    assert data["stock_quantity"] == 20
    assert data["image_url"] == (
        "https://example.com/images/kids-t-shirt.jpg"
    )
    assert data["is_active"] is True


def test_get_product_not_found(client):
    product_id = uuid4()

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."


def test_update_product(admin_client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Men",
        category_slug="men",
        sub_category_name="Shirts",
        sub_category_slug="shirts",
    )

    create_response = create_product(
        admin_client,
        sub_category.id,
        "Men's Shirt",
        "mens-shirt",
        price=1999,
        stock_quantity=25,
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = admin_client.patch(
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
    assert data["image_url"] == (
        "https://example.com/images/mens-shirt.jpg"
    )
    assert data["is_active"] is True


def test_create_duplicate_product(admin_client, db_session):
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

    first_response = admin_client.post(
        "/products",
        json=product_data,
    )

    assert first_response.status_code == 201

    second_response = admin_client.post(
        "/products",
        json=product_data,
    )

    assert second_response.status_code == 409


def test_update_product_not_found(admin_client):
    product_id = uuid4()

    response = admin_client.patch(
        f"/products/{product_id}",
        json={
            "name": "Updated Product",
        },
    )

    assert response.status_code == 404


def test_delete_product(admin_client, db_session):
    category, sub_category = create_category_and_sub_category(
        db_session,
        category_name="Kids",
        category_slug="kids",
        sub_category_name="T-Shirts",
        sub_category_slug="t-shirts",
    )

    create_response = create_product(
        admin_client,
        sub_category.id,
        "Kids T-Shirt",
        "kids-t-shirt",
        price=2999,
        stock_quantity=10,
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = admin_client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 204

    get_response = admin_client.get(
        f"/products/{product_id}"
    )

    assert get_response.status_code == 404


def test_delete_product_not_found(admin_client):
    product_id = uuid4()

    response = admin_client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 404


def test_customer_cannot_create_product(customer_client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
    )

    response = customer_client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category.id),
            "name": "Test Product",
            "slug": "test-product",
            "description": "Test product",
            "price": 1999,
            "currency": "USD",
            "stock_quantity": 10,
            "image_url": "https://example.com/test.jpg",
            "is_active": True,
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_unauthenticated_cannot_create_product(client, db_session):
    _, sub_category = create_category_and_sub_category(
        db_session,
    )

    response = client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category.id),
            "name": "Test Product",
            "slug": "test-product",
            "description": "Test product",
            "price": 1999,
            "currency": "USD",
            "stock_quantity": 10,
            "image_url": "https://example.com/test.jpg",
            "is_active": True,
        },
    )

    assert response.status_code == 401


def test_customer_cannot_update_product(
    customer_client,
    db_session,
):
    _, sub_category = create_category_and_sub_category(
        db_session,
    )

    product = Product(
        sub_category_id=sub_category.id,
        name="Test Product",
        slug="test-product",
        description="Test product description",
        price=1999,
        currency="USD",
        stock_quantity=25,
        image_url="https://example.com/test.jpg",
        is_active=True,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = customer_client.patch(
        f"/products/{product.id}",
        json={
            "name": "Updated Product",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_customer_cannot_delete_product(
    customer_client,
    db_session,
):
    _, sub_category = create_category_and_sub_category(
        db_session,
    )

    product = Product(
        sub_category_id=sub_category.id,
        name="Test Product",
        slug="test-product",
        description="Test product description",
        price=1999,
        currency="USD",
        stock_quantity=25,
        image_url="https://example.com/test.jpg",
        is_active=True,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = customer_client.delete(
        f"/products/{product.id}"
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_unauthenticated_cannot_update_product(
    client,
    db_session,
):
    _, sub_category = create_category_and_sub_category(
        db_session,
    )

    response = client.patch(
        f"/products/{uuid4()}",
        json={
            "name": "Updated Product",
        },
    )

    assert response.status_code == 401
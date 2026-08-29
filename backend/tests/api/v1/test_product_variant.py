from uuid import uuid4

from app.models.product_variant import ProductVariant

from tests.api.v1.test_product import create_category_and_sub_category


def create_product(admin_client, db_session):
    _, sub_category = create_category_and_sub_category(
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
            "description": "Men's cotton shirt",
            "price": 2499,
            "currency": "USD",
            "stock_quantity": 100,
            "image_url": "https://example.com/images/shirt.jpg",
            "is_active": True,
        },
    )

    assert response.status_code == 201

    return response.json()


def create_variant(
    admin_client,
    product_id,
    sku="SHIRT-BLK-M",
    size="M",
    color="Black",
    material="Cotton",
    price=2499,
    stock_quantity=10,
    is_active=True,
):
    return admin_client.post(
        f"/products/{product_id}/variants",
        json={
            "sku": sku,
            "size": size,
            "color": color,
            "material": material,
            "price": price,
            "stock_quantity": stock_quantity,
            "is_active": is_active,
        },
    )


def test_create_product_variant(admin_client, db_session):
    product = create_product(admin_client, db_session)

    response = create_variant(
        admin_client,
        product["id"],
    )

    assert response.status_code == 201

    data = response.json()

    assert data["product_id"] == product["id"]
    assert data["sku"] == "SHIRT-BLK-M"
    assert data["size"] == "M"
    assert data["color"] == "Black"
    assert data["material"] == "Cotton"
    assert data["price"] == 2499
    assert data["stock_quantity"] == 10
    assert data["is_active"] is True

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

    variant = db_session.get(
        ProductVariant,
        data["id"],
    )

    assert variant is not None
    assert str(variant.product_id) == product["id"]
    assert variant.sku == "SHIRT-BLK-M"
    assert variant.size == "M"
    assert variant.color == "Black"
    assert variant.material == "Cotton"
    assert variant.price == 2499
    assert variant.stock_quantity == 10


def test_create_product_variant_product_not_found(admin_client):
    product_id = uuid4()

    response = create_variant(
        admin_client,
        str(product_id),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."


def test_create_duplicate_product_variant_sku(admin_client, db_session):
    product = create_product(admin_client, db_session)

    first_response = create_variant(
        admin_client,
        product["id"],
        sku="SHIRT-BLK-M",
    )

    assert first_response.status_code == 201

    second_response = create_variant(
        admin_client,
        product["id"],
        sku="SHIRT-BLK-M",
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"]
        == "Product variant with this SKU already exists."
    )


def test_get_product_variants(admin_client, client, db_session):
    product = create_product(admin_client, db_session)

    first_response = create_variant(
        admin_client,
        product["id"],
        sku="SHIRT-BLK-M",
    )

    second_response = create_variant(
        admin_client,
        product["id"],
        sku="SHIRT-BLK-L",
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    response = client.get(
        f"/products/{product['id']}/variants"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["product_id"] == product["id"]
    assert data[1]["product_id"] == product["id"]

    skus = {variant["sku"] for variant in data}

    assert skus == {
        "SHIRT-BLK-M",
        "SHIRT-BLK-L",
    }


def test_get_product_variants_product_not_found(client):
    product_id = uuid4()

    response = client.get(
        f"/products/{product_id}/variants"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."


def test_get_product_variant_by_id(admin_client, client, db_session):
    product = create_product(admin_client, db_session)

    create_response = create_variant(
        admin_client,
        product["id"],
    )

    assert create_response.status_code == 201

    variant_id = create_response.json()["id"]

    response = client.get(
        f"/products/{product['id']}/variants/{variant_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == variant_id
    assert data["product_id"] == product["id"]
    assert data["sku"] == "SHIRT-BLK-M"
    assert data["size"] == "M"
    assert data["color"] == "Black"
    assert data["material"] == "Cotton"


def test_get_product_variant_not_found(admin_client, client, db_session):
    product = create_product(admin_client, db_session)

    variant_id = uuid4()

    response = client.get(
        f"/products/{product['id']}/variants/{variant_id}"
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Product variant not found."
    )


def test_product_variant_cannot_be_accessed_through_another_product(
    admin_client,
    client,
    db_session,
):
    product_one = create_product(admin_client, db_session)

    # Create a second product with a different subcategory.
    _, sub_category_two = create_category_and_sub_category(
        db_session,
        category_name="Women",
        category_slug="women",
        sub_category_name="Dresses",
        sub_category_slug="dresses",
    )

    product_two_response = admin_client.post(
        "/products",
        json={
            "sub_category_id": str(sub_category_two.id),
            "name": "Women's Dress",
            "slug": "womens-dress",
            "description": "Women's summer dress",
            "price": 2999,
            "currency": "USD",
            "stock_quantity": 50,
            "image_url": "https://example.com/images/dress.jpg",
            "is_active": True,
        },
    )

    assert product_two_response.status_code == 201

    product_two = product_two_response.json()

    variant_response = create_variant(
        admin_client,
        product_two["id"],
        sku="DRESS-BLK-M",
    )

    assert variant_response.status_code == 201

    variant_id = variant_response.json()["id"]

    response = client.get(
        f"/products/{product_one['id']}/variants/{variant_id}"
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Product variant not found."
    )


def test_update_product_variant(admin_client, db_session):
    product = create_product(admin_client, db_session)

    create_response = create_variant(
        admin_client,
        product["id"],
    )

    assert create_response.status_code == 201

    variant_id = create_response.json()["id"]

    response = admin_client.patch(
        f"/products/{product['id']}/variants/{variant_id}",
        json={
            "sku": "SHIRT-BLK-L",
            "size": "L",
            "price": 2699,
            "stock_quantity": 20,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == variant_id
    assert data["product_id"] == product["id"]
    assert data["sku"] == "SHIRT-BLK-L"
    assert data["size"] == "L"
    assert data["color"] == "Black"
    assert data["material"] == "Cotton"
    assert data["price"] == 2699
    assert data["stock_quantity"] == 20


def test_update_product_variant_duplicate_sku(
    admin_client,
    db_session,
):
    product = create_product(admin_client, db_session)

    first_response = create_variant(
        admin_client,
        product["id"],
        sku="SHIRT-BLK-M",
    )

    second_response = create_variant(
        admin_client,
        product["id"],
        sku="SHIRT-BLK-L",
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    second_variant_id = second_response.json()["id"]

    response = admin_client.patch(
        f"/products/{product['id']}/variants/{second_variant_id}",
        json={
            "sku": "SHIRT-BLK-M",
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "Product variant with this SKU already exists."
    )


def test_delete_product_variant(admin_client, client, db_session):
    product = create_product(admin_client, db_session)

    create_response = create_variant(
        admin_client,
        product["id"],
    )

    assert create_response.status_code == 201

    variant_id = create_response.json()["id"]

    response = admin_client.delete(
        f"/products/{product['id']}/variants/{variant_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/products/{product['id']}/variants/{variant_id}"
    )

    assert get_response.status_code == 404


def test_delete_product_variant_not_found(admin_client, db_session):
    product = create_product(admin_client, db_session)

    variant_id = uuid4()

    response = admin_client.delete(
        f"/products/{product['id']}/variants/{variant_id}"
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Product variant not found."
    )


def test_create_product_variant_negative_price(admin_client, db_session):
    product = create_product(admin_client, db_session)

    response = create_variant(
        admin_client,
        product["id"],
        price=-1,
    )

    assert response.status_code == 422


def test_create_product_variant_negative_stock(admin_client, db_session):
    product = create_product(admin_client, db_session)

    response = create_variant(
        admin_client,
        product["id"],
        stock_quantity=-1,
    )

    assert response.status_code == 422


def test_create_product_variant_empty_size(admin_client, db_session):
    product = create_product(admin_client, db_session)

    response = create_variant(
        admin_client,
        product["id"],
        size="",
    )

    assert response.status_code == 422


def test_update_product_variant_negative_stock(admin_client, db_session):
    product = create_product(admin_client, db_session)

    create_response = create_variant(
        admin_client,
        product["id"],
    )

    variant_id = create_response.json()["id"]

    response = admin_client.patch(
        f"/products/{product['id']}/variants/{variant_id}",
        json={
            "stock_quantity": -1,
        },
    )

    assert response.status_code == 422


def test_customer_cannot_create_product_variant(
    customer_client,
    admin_client,
    db_session,
):
    product = create_product(admin_client, db_session)

    response = customer_client.post(
        f"/products/{product['id']}/variants",
        json={
            "sku": "SHIRT-BLK-M",
            "size": "M",
            "color": "Black",
            "material": "Cotton",
            "price": 2499,
            "stock_quantity": 10,
            "is_active": True,
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_customer_cannot_update_product_variant(
    customer_client,
    admin_client,
    db_session,
):
    product = create_product(admin_client, db_session)

    create_response = create_variant(
        admin_client,
        product["id"],
    )

    assert create_response.status_code == 201

    variant_id = create_response.json()["id"]

    response = customer_client.patch(
        f"/products/{product['id']}/variants/{variant_id}",
        json={
            "size": "L",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_customer_cannot_delete_product_variant(
    customer_client,
    admin_client,
    db_session,
):
    product = create_product(admin_client, db_session)

    create_response = create_variant(
        admin_client,
        product["id"],
    )

    assert create_response.status_code == 201

    variant_id = create_response.json()["id"]

    response = customer_client.delete(
        f"/products/{product['id']}/variants/{variant_id}"
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_unauthenticated_cannot_create_product_variant(
    admin_client,
    client,
    db_session,
):
    product = create_product(admin_client, db_session)

    response = client.post(
        f"/products/{product['id']}/variants",
        json={
            "sku": "SHIRT-BLK-M",
            "size": "M",
            "color": "Black",
            "material": "Cotton",
            "price": 2499,
            "stock_quantity": 10,
            "is_active": True,
        },
    )

    assert response.status_code == 401


def test_unauthenticated_cannot_update_product_variant(
    client,
    admin_client,
    db_session,
):
    product = create_product(admin_client, db_session)

    create_response = create_variant(
        admin_client,
        product["id"],
    )

    assert create_response.status_code == 201

    variant_id = create_response.json()["id"]

    response = client.patch(
        f"/products/{product['id']}/variants/{variant_id}",
        json={
            "size": "L",
        },
    )

    assert response.status_code == 401


def test_unauthenticated_cannot_delete_product_variant(
    client,
    admin_client,
    db_session,
):
    product = create_product(admin_client, db_session)

    create_response = create_variant(
        admin_client,
        product["id"],
    )

    assert create_response.status_code == 201

    variant_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product['id']}/variants/{variant_id}"
    )

    assert response.status_code == 401
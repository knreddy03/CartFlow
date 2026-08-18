from uuid import uuid4

from app.models.category import Category
from app.models.sub_category import SubCategory


def create_category(client):
    response = client.post(
        "/categories",
        json={
            "name": "Men",
            "slug": "men",
            "description": "Men's clothing",
            "image_url": "https://example.com/images/men.jpg",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_create_sub_category(client, db_session):
    category_id = create_category(client)

    response = client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "Shoes",
            "slug": "shoes",
            "description": "Men's shoes",
            "image_url": "https://example.com/images/shoes.jpg",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["category_id"] == category_id
    assert data["name"] == "Shoes"
    assert data["slug"] == "shoes"
    assert data["description"] == "Men's shoes"
    assert data["image_url"] == "https://example.com/images/shoes.jpg"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

    sub_category = db_session.get(SubCategory, data["id"])

    assert sub_category is not None
    assert str(sub_category.category_id) == category_id
    assert sub_category.name == "Shoes"
    assert sub_category.slug == "shoes"


def test_create_sub_category_category_not_found(client):
    category_id = str(uuid4())

    response = client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "Shoes",
            "slug": "shoes",
            "description": "Men's shoes",
            "image_url": "https://example.com/images/shoes.jpg",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."


def test_get_sub_categories(client):
    category_id = create_category(client)

    client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "Shoes",
            "slug": "shoes",
            "description": "Men's shoes",
            "image_url": "https://example.com/images/shoes.jpg",
        },
    )

    client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "Shirts",
            "slug": "shirts",
            "description": "Men's shirts",
            "image_url": "https://example.com/images/shirts.jpg",
        },
    )

    response = client.get("/sub-categories")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Shirts"
    assert data[1]["name"] == "Shoes"


def test_get_sub_category_by_id(client):
    category_id = create_category(client)

    create_response = client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "Pants",
            "slug": "pants",
            "description": "Men's pants",
            "image_url": "https://example.com/images/pants.jpg",
        },
    )

    assert create_response.status_code == 201

    sub_category_id = create_response.json()["id"]

    response = client.get(
        f"/sub-categories/{sub_category_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sub_category_id
    assert data["category_id"] == category_id
    assert data["name"] == "Pants"
    assert data["slug"] == "pants"


def test_get_sub_category_not_found(client):
    sub_category_id = uuid4()

    response = client.get(
        f"/sub-categories/{sub_category_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sub Category not found."


def test_get_sub_categories_by_category(client):
    category_id = create_category(client)

    client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "Shoes",
            "slug": "shoes",
            "description": "Men's shoes",
            "image_url": "https://example.com/images/shoes.jpg",
        },
    )

    client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "T-Shirts",
            "slug": "t-shirts",
            "description": "Men's t-shirts",
            "image_url": "https://example.com/images/tshirts.jpg",
        },
    )

    response = client.get(
        f"/sub-categories/category/{category_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Shoes"
    assert data[1]["name"] == "T-Shirts"


def test_get_sub_categories_by_category_not_found(client):
    category_id = uuid4()

    response = client.get(
        f"/sub-categories/category/{category_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."


def test_update_sub_category(client):
    category_id = create_category(client)

    create_response = client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "Shoes",
            "slug": "shoes",
            "description": "Men's shoes",
            "image_url": "https://example.com/images/shoes.jpg",
        },
    )

    assert create_response.status_code == 201

    sub_category_id = create_response.json()["id"]

    response = client.patch(
        f"/sub-categories/{sub_category_id}",
        json={
            "name": "Running Shoes",
            "description": "Men's running shoes",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sub_category_id
    assert data["name"] == "Running Shoes"
    assert data["slug"] == "shoes"
    assert data["description"] == "Men's running shoes"


def test_update_sub_category_not_found(client):
    sub_category_id = uuid4()

    response = client.patch(
        f"/sub-categories/{sub_category_id}",
        json={
            "name": "Updated Category",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sub Category not found."


def test_create_duplicate_sub_category(client):
    category_id = create_category(client)

    sub_category_data = {
        "category_id": category_id,
        "name": "Shoes",
        "slug": "shoes",
        "description": "Men's shoes",
        "image_url": "https://example.com/images/shoes.jpg",
    }

    first_response = client.post(
        "/sub-categories",
        json=sub_category_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/sub-categories",
        json=sub_category_data,
    )

    assert second_response.status_code == 409


def test_delete_sub_category(client):
    category_id = create_category(client)

    create_response = client.post(
        "/sub-categories",
        json={
            "category_id": category_id,
            "name": "Shoes",
            "slug": "shoes",
            "description": "Men's shoes",
            "image_url": "https://example.com/images/shoes.jpg",
        },
    )

    assert create_response.status_code == 201

    sub_category_id = create_response.json()["id"]

    response = client.delete(
        f"/sub-categories/{sub_category_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/sub-categories/{sub_category_id}"
    )

    assert get_response.status_code == 404


def test_delete_sub_category_not_found(client):
    sub_category_id = uuid4()

    response = client.delete(
        f"/sub-categories/{sub_category_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sub Category not found."
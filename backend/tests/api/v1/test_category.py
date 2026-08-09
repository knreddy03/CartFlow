from app.models.category import Category
from uuid import uuid4


def test_create_category(client, db_session):
    response = client.post(
        "/categories",
        json={
            "name": "Men",
            "slug": "men",
            "description": "Men's clothing and accessories",
            "image_url": "https://example.com/images/men.jpg",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Men"
    assert data["slug"] == "men"
    assert data["description"] == "Men's clothing and accessories"
    assert data["image_url"] == "https://example.com/images/men.jpg"
    assert "id" in data
    assert "created_at" in data

    category = db_session.get(Category, data["id"])

    assert category is not None
    assert category.name == "Men"
    assert category.slug == "men"
    assert category.description == "Men's clothing and accessories"
    assert category.image_url == "https://example.com/images/men.jpg"



def test_get_categories(client):
    create_response = client.post(
        "/categories",
        json={
            "name": "Women",
            "slug": "women",
            "description": "Women's clothing and accessories",
            "image_url": "https://example.com/images/women.jpg",
        },
    )

    assert create_response.status_code == 201

    response = client.get("/categories")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Women"
    assert data[0]["slug"] == "women"
    assert data[0]["description"] == "Women's clothing and accessories"
    assert data[0]["image_url"] == "https://example.com/images/women.jpg"


def test_get_category_by_id(client):
    create_response = client.post(
        "/categories",
        json={
            "name": "Kids",
            "slug": "kids",
            "description": "Kids clothing and accessories",
            "image_url": "https://example.com/images/kids.jpg",
        },
    )

    assert create_response.status_code == 201

    created_category = create_response.json()
    category_id = created_category["id"]

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == category_id
    assert data["name"] == "Kids"
    assert data["slug"] == "kids"
    assert data["description"] == "Kids clothing and accessories"
    assert data["image_url"] == "https://example.com/images/kids.jpg"


def test_get_category_not_found(client):
    category_id = uuid4()

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."


def test_update_category(client):
    create_response = client.post(
        "/categories",
        json={
            "name": "Men",
            "slug": "men",
            "description": "Men's clothing",
            "image_url": "https://example.com/images/men.jpg",
        },
    )

    assert create_response.status_code == 201

    category_id = create_response.json()["id"]

    response = client.patch(
        f"/categories/{category_id}",
        json={
            "name": "Men's Clothing",
            "description": "Men's clothing and accessories",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == category_id
    assert data["name"] == "Men's Clothing"
    assert data["slug"] == "men"
    assert data["description"] == "Men's clothing and accessories"
    assert data["image_url"] == "https://example.com/images/men.jpg"


def test_create_duplicate_category(client):
    category_data = {
        "name": "Electronics",
        "slug": "electronics",
        "description": "Electronic products",
        "image_url": "https://example.com/images/electronics.jpg",
    }

    first_response = client.post(
        "/categories",
        json=category_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/categories",
        json=category_data,
    )

    assert second_response.status_code == 409



def test_update_category_not_found(client):
    category_id = uuid4()

    response = client.patch(
        f"/categories/{category_id}",
        json={
            "name": "Updated Category",
        },
    )

    assert response.status_code == 404


def test_delete_category(client):
    create_response = client.post(
        "/categories",
        json={
            "name": "Books",
            "slug": "books",
            "description": "Books and literature",
            "image_url": "https://example.com/images/books.jpg",
        },
    )

    assert create_response.status_code == 201

    category_id = create_response.json()["id"]

    response = client.delete(
        f"/categories/{category_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/categories/{category_id}"
    )

    assert get_response.status_code == 404


def test_delete_category_not_found(client):
    category_id = uuid4()

    response = client.delete(
        f"/categories/{category_id}"
    )

    assert response.status_code == 404

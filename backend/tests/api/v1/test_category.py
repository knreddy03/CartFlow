from app.models.category import Category
from uuid import uuid4


def test_create_category(admin_client, db_session):
    response = admin_client.post(
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



def test_get_categories(client, db_session):
    category = Category(
        name="Women",
        slug="women",
        description="Women's clothing and accessories",
        image_url="https://example.com/images/women.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = client.get("/categories")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Women"
    assert data[0]["slug"] == "women"
    assert data[0]["description"] == "Women's clothing and accessories"
    assert data[0]["image_url"] == "https://example.com/images/women.jpg"


def test_get_category_by_id(client, db_session):
    category = Category(
        name="Kids",
        slug="kids",
        description="Kids clothing and accessories",
        image_url="https://example.com/images/kids.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = client.get(f"/categories/{category.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(category.id)
    assert data["name"] == "Kids"
    assert data["slug"] == "kids"
    assert data["description"] == "Kids clothing and accessories"
    assert data["image_url"] == "https://example.com/images/kids.jpg"


def test_get_category_not_found(client):
    category_id = uuid4()

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."


def test_update_category(admin_client):
    create_response = admin_client.post(
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

    response = admin_client.patch(
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


def test_create_duplicate_category(admin_client):
    category_data = {
        "name": "Electronics",
        "slug": "electronics",
        "description": "Electronic products",
        "image_url": "https://example.com/images/electronics.jpg",
    }

    first_response = admin_client.post(
        "/categories",
        json=category_data,
    )

    assert first_response.status_code == 201

    second_response = admin_client.post(
        "/categories",
        json=category_data,
    )

    assert second_response.status_code == 409



def test_update_category_not_found(admin_client):
    category_id = uuid4()

    response = admin_client.patch(
        f"/categories/{category_id}",
        json={
            "name": "Updated Category",
        },
    )

    assert response.status_code == 404


def test_delete_category(admin_client):
    create_response = admin_client.post(
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

    response = admin_client.delete(
        f"/categories/{category_id}"
    )

    assert response.status_code == 204

    get_response = admin_client.get(
        f"/categories/{category_id}"
    )

    assert get_response.status_code == 404


def test_delete_category_not_found(admin_client):
    category_id = uuid4()

    response = admin_client.delete(
        f"/categories/{category_id}"
    )

    assert response.status_code == 404


def test_customer_cannot_create_category(customer_client):
    response = customer_client.post(
        "/categories",
        json={
            "name": "Electronics",
            "slug": "electronics",
            "description": "Electronic products",
            "image_url": "https://example.com/images/electronics.jpg",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_customer_cannot_update_category(
    customer_client,
    db_session,
):
    category = Category(
        name="Electronics",
        slug="electronics",
        description="Electronic products",
        image_url="https://example.com/images/electronics.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = customer_client.patch(
        f"/categories/{category.id}",
        json={
            "name": "Updated Electronics",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_customer_cannot_delete_category(
    customer_client,
    db_session,
):
    category = Category(
        name="Electronics",
        slug="electronics",
        description="Electronic products",
        image_url="https://example.com/images/electronics.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = customer_client.delete(
        f"/categories/{category.id}",
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_unauthenticated_cannot_create_category(client):
    response = client.post(
        "/categories",
        json={
            "name": "Electronics",
            "slug": "electronics",
            "description": "Electronic products",
            "image_url": "https://example.com/images/electronics.jpg",
        },
    )

    assert response.status_code == 401


def test_unauthenticated_cannot_update_category(
    client,
    db_session,
):
    category = Category(
        name="Electronics",
        slug="electronics",
        description="Electronic products",
        image_url="https://example.com/images/electronics.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = client.patch(
        f"/categories/{category.id}",
        json={
            "name": "Updated Electronics",
        },
    )

    assert response.status_code == 401


def test_unauthenticated_cannot_delete_category(
    client,
    db_session,
):
    category = Category(
        name="Electronics",
        slug="electronics",
        description="Electronic products",
        image_url="https://example.com/images/electronics.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = client.delete(
        f"/categories/{category.id}",
    )

    assert response.status_code == 401
from uuid import uuid4

from app.models.category import Category
from app.models.sub_category import SubCategory


def create_category(admin_client):
    response = admin_client.post(
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


def test_create_sub_category(admin_client, db_session):
    category_id = create_category(admin_client)

    response = admin_client.post(
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


def test_create_sub_category_category_not_found(admin_client):
    category_id = str(uuid4())

    response = admin_client.post(
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


def test_get_sub_categories(client, db_session):
    category = Category(
        name="Men",
        slug="men",
        description= "Men's clothing",
        image_url="https://example.com/images/men.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    sub_category1 = SubCategory(
        category_id=category.id,
        name="Shoes",
        slug="shoes",
        description="Men's shoes",
        image_url="https://example.com/images/shoes.jpg",
    )

    sub_category2 = SubCategory(
        category_id=category.id,
        name="T-Shirts",
        slug="t-shirts",
        description="Men's t-shirts",
        image_url="https://example.com/images/tshirts.jpg",
    )

    db_session.add_all([sub_category1, sub_category2])
    db_session.commit()
    
    response = client.get("/sub-categories")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    names = {item["name"] for item in data}
    assert names == {"Shoes", "T-Shirts"}


def test_get_sub_category_by_id(client, db_session):
    category = Category(
            name="Men",
            slug="men",
            description= "Men's clothing",
            image_url="https://example.com/images/men.jpg",
        )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    sub_category = SubCategory(
        category_id=category.id,
        name="Pants",
        slug="pants",
        description="Men's pants",
        image_url="https://example.com/images/pants.jpg",
    )

    db_session.add(sub_category)
    db_session.commit()
    db_session.refresh(sub_category)

    response = client.get(
        f"/sub-categories/{sub_category.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(sub_category.id)
    assert data["category_id"] == str(category.id)
    assert data["name"] == "Pants"
    assert data["slug"] == "pants"


def test_get_sub_category_not_found(client):
    sub_category_id = uuid4()

    response = client.get(
        f"/sub-categories/{sub_category_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sub Category not found."


def test_get_sub_categories_by_category(client, db_session):
    category = Category(
            name="Men",
            slug="men",
            description= "Men's clothing",
            image_url="https://example.com/images/men.jpg",
        )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    sub_category1 = SubCategory(
        category_id=category.id,
        name="Shoes",
        slug="shoes",
        description="Men's shoes",
        image_url="https://example.com/images/shoes.jpg",
    )

    sub_category2 = SubCategory(
        category_id=category.id,
        name="T-Shirts",
        slug="t-shirts",
        description="Men's t-shirts",
        image_url="https://example.com/images/tshirts.jpg",
    )

    db_session.add_all([sub_category1, sub_category2])
    db_session.commit()

    response = client.get(
        f"/sub-categories/category/{category.id}"
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


def test_update_sub_category(admin_client):
    category_id = create_category(admin_client)

    create_response = admin_client.post(
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

    response = admin_client.patch(
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


def test_update_sub_category_not_found(admin_client):
    sub_category_id = uuid4()

    response = admin_client.patch(
        f"/sub-categories/{sub_category_id}",
        json={
            "name": "Updated Category",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sub Category not found."


def test_create_duplicate_sub_category(admin_client):
    category_id = create_category(admin_client)

    sub_category_data = {
        "category_id": category_id,
        "name": "Shoes",
        "slug": "shoes",
        "description": "Men's shoes",
        "image_url": "https://example.com/images/shoes.jpg",
    }

    first_response = admin_client.post(
        "/sub-categories",
        json=sub_category_data,
    )

    assert first_response.status_code == 201

    second_response = admin_client.post(
        "/sub-categories",
        json=sub_category_data,
    )

    assert second_response.status_code == 409


def test_delete_sub_category(admin_client):
    category_id = create_category(admin_client)

    create_response = admin_client.post(
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

    response = admin_client.delete(
        f"/sub-categories/{sub_category_id}"
    )

    assert response.status_code == 204

    get_response = admin_client.get(
        f"/sub-categories/{sub_category_id}"
    )

    assert get_response.status_code == 404


def test_delete_sub_category_not_found(admin_client):
    sub_category_id = uuid4()

    response = admin_client.delete(
        f"/sub-categories/{sub_category_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sub Category not found."


def test_customer_cannot_create_sub_category(
    customer_client,
    db_session,
):
    category = Category(
        name="Men",
        slug="men",
        description="Men's clothing",
        image_url="https://example.com/images/men.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = customer_client.post(
        "/sub-categories",
        json={
            "category_id": str(category.id),
            "name": "Shoes",
            "slug": "shoes",
            "description": "Men's shoes",
            "image_url": "https://example.com/images/shoes.jpg",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_customer_cannot_update_sub_category(
    customer_client,
    db_session,
):
    category = Category(
        name="Men",
        slug="men",
        description="Men's clothing",
        image_url="https://example.com/images/men.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    sub_category = SubCategory(
        category_id=category.id,
        name="Shoes",
        slug="shoes",
        description="Men's shoes",
        image_url="https://example.com/images/shoes.jpg",
    )

    db_session.add(sub_category)
    db_session.commit()
    db_session.refresh(sub_category)

    response = customer_client.patch(
        f"/sub-categories/{sub_category.id}",
        json={
            "name": "Running Shoes",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_customer_cannot_delete_sub_category(
    customer_client,
    db_session,
):
    category = Category(
        name="Men",
        slug="men",
        description="Men's clothing",
        image_url="https://example.com/images/men.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    sub_category = SubCategory(
        category_id=category.id,
        name="Shoes",
        slug="shoes",
        description="Men's shoes",
        image_url="https://example.com/images/shoes.jpg",
    )

    db_session.add(sub_category)
    db_session.commit()
    db_session.refresh(sub_category)

    response = customer_client.delete(
        f"/sub-categories/{sub_category.id}"
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_unauthenticated_cannot_create_sub_category(
    client,
    db_session,
):
    category = Category(
        name="Men",
        slug="men",
        description="Men's clothing",
        image_url="https://example.com/images/men.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = client.post(
        "/sub-categories",
        json={
            "category_id": str(category.id),
            "name": "Shoes",
            "slug": "shoes",
            "description": "Men's shoes",
            "image_url": "https://example.com/images/shoes.jpg",
        },
    )

    assert response.status_code == 401


def test_unauthenticated_cannot_update_sub_category(
    client,
    db_session,
):
    category = Category(
        name="Men",
        slug="men",
        description="Men's clothing",
        image_url="https://example.com/images/men.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    sub_category = SubCategory(
        category_id=category.id,
        name="Shoes",
        slug="shoes",
        description="Men's shoes",
        image_url="https://example.com/images/shoes.jpg",
    )

    db_session.add(sub_category)
    db_session.commit()
    db_session.refresh(sub_category)

    response = client.patch(
        f"/sub-categories/{sub_category.id}",
        json={
            "name": "Running Shoes",
        },
    )

    assert response.status_code == 401


def test_unauthenticated_cannot_delete_sub_category(
    client,
    db_session,
):
    category = Category(
        name="Men",
        slug="men",
        description="Men's clothing",
        image_url="https://example.com/images/men.jpg",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    sub_category = SubCategory(
        category_id=category.id,
        name="Shoes",
        slug="shoes",
        description="Men's shoes",
        image_url="https://example.com/images/shoes.jpg",
    )

    db_session.add(sub_category)
    db_session.commit()
    db_session.refresh(sub_category)

    response = client.delete(
        f"/sub-categories/{sub_category.id}"
    )

    assert response.status_code == 401
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.auth import create_access_token
from app.db.database import get_db
from app.main import app

from datetime import date

from app.dependencies.user import get_current_user, get_current_user_id
from app.models.user import User, UserRole


test_engine = create_engine(
    settings.test_database_url,
    pool_pre_ping=True,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture
def db_session():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def authenticated_user(db_session):
    user = User(
        first_name="Test",
        last_name="User",
        mobile="1234567890",
        email="test@example.com",
        password="hashed-password",
        date_of_birth=date(1995, 1, 1),
        role=UserRole.CUSTOMER,
        is_verified=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def admin_user(db_session):
    user = User(
        first_name="Admin",
        last_name="User",
        mobile="9876543210",
        email="admin@example.com",
        password="hashed-password",
        date_of_birth=date(1990, 1, 1),
        role=UserRole.ADMIN,
        is_verified=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def authenticated_client(client, authenticated_user):
    def override_get_current_user_id():
        return authenticated_user.id

    app.dependency_overrides[get_current_user_id] = (
        override_get_current_user_id
    )

    yield client

    app.dependency_overrides.pop(
        get_current_user_id,
        None,
    )


@pytest.fixture
def customer_client(db_session, authenticated_user):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    token = create_access_token(authenticated_user.id)

    with TestClient(app) as test_client:
        test_client.headers.update(
            {"Authorization": f"Bearer {token}"}
        )

        yield test_client

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def admin_client(db_session, admin_user):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    token = create_access_token(admin_user.id)

    with TestClient(app) as test_client:
        test_client.headers.update(
            {"Authorization": f"Bearer {token}"}
        )

        yield test_client

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(autouse=True)
def clean_database():
    with test_engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    email_verification_tokens,
                    refresh_tokens,
                    carts,
                    cart_items,
                    products,
                    sub_categories,
                    categories,
                    users
                RESTART IDENTITY CASCADE
                """
            )
        )

    yield

    with test_engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    email_verification_tokens,
                    refresh_tokens,
                    carts,
                    cart_items,
                    products,
                    sub_categories,
                    categories,
                    users
                RESTART IDENTITY CASCADE
                """
            )
        )
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.refresh_token_service import RefreshTokenService
from app.services.email_verification_service import EmailVerificationService
from app.services.category_service import CategoryService
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.sub_category_service import SubCategoryService

from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.cart_item_repository import CartItemRepository


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)


def get_refresh_token_service(
    db: Session = Depends(get_db),
) -> RefreshTokenService:
    return RefreshTokenService(db)


def get_email_verification_service(
    db: Session = Depends(get_db),
) -> EmailVerificationService:
    return EmailVerificationService(db)


def get_auth_service(
    db: Session = Depends(get_db),
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service),
    email_verification_service: EmailVerificationService = Depends(get_email_verification_service),
) -> AuthService:

    return AuthService(db, refresh_token_service, email_verification_service,)


def get_category_service(
    db: Session = Depends(get_db),
) -> CategoryService:
    return CategoryService(db)


def get_product_service(
    db: Session = Depends(get_db),
) -> ProductService:
    return ProductService(db)


def get_cart_service(
    db: Session = Depends(get_db),
) -> CartService:
    return CartService(
        db=db,
        cart_repository=CartRepository(db),
        cart_item_repository=CartItemRepository(db),
        product_repository=ProductRepository(db),
        )


def get_sub_category_service(
    db: Session = Depends(get_db),
) -> SubCategoryService:
    return SubCategoryService(db)

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.refresh_token_service import RefreshTokenService
from app.services.email_verification_service import EmailVerificationService
from app.services.category_service import CategoryService
from app.services.product_service import ProductService


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
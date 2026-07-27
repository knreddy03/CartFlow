from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.refresh_token_service import RefreshTokenService


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:

    refresh_token_service = RefreshTokenService(db)
    return AuthService(db, refresh_token_service)


def get_refresh_token_service(
    db: Session = Depends(get_db),
) -> RefreshTokenService:
    return RefreshTokenService(db)
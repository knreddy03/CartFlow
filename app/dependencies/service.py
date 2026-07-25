from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.services.auth_service import AuthService


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    return AuthService(db)
from sqlalchemy.orm import Session
from app.core.auth import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import RefreshTokenRequest, RegisterRequest, LoginRequest, TokenResponse
from app.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
)
from app.services.refresh_token_service import RefreshTokenService

class AuthService:

    def __init__(self, db: Session, refresh_token_service: RefreshTokenService):
        self.db = db
        self.user_repository = UserRepository(db)
        self.refresh_token_service = refresh_token_service


    def register(self, data: RegisterRequest) -> User:

        if self.user_repository.get_by_email(data.email):
            raise UserAlreadyExistsError("User with this email already exists.")
        
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            mobile=data.mobile,
            email=data.email,
            password=hash_password(data.password),
            date_of_birth=data.date_of_birth,
        )

        try:
            self.user_repository.add(user)

            self.db.commit()
            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise
    

    def login(self, data: LoginRequest) -> dict:
        user = self.user_repository.get_by_email(data.email)
        if not user:
            raise InvalidCredentialsError("Invalid email or password.")
        
        if not verify_password(data.password, user.password):
            raise InvalidCredentialsError("Invalid email or password.")
        
        access_token = create_access_token(user.id)
        refresh_token = self.refresh_token_service.create_token(user.id)

        try:
            self.db.commit()
            self.db.refresh(user)
                
        except Exception:
            self.db.rollback()
            raise
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }


    def refresh(self,data: RefreshTokenRequest) -> TokenResponse:
        try:
            access_token, refresh_token = (
                self.refresh_token_service.rotate_token(
                    data.refresh_token
                )
            )
            
            self.db.commit()
                
        except Exception:
            self.db.rollback()
            raise

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


    def logout(self, data: RefreshTokenRequest) -> None:
        self.refresh_token_service.revoke_token(
        data.refresh_token
        )
        try:
            self.db.commit()
                
        except Exception:
            self.db.rollback()
            raise
from sqlalchemy.orm import Session
from app.core.auth import generate_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
)


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)


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
        
        access_token = generate_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
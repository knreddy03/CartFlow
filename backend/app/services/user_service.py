from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from uuid import UUID
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserUpdate
from app.exceptions.user_exceptions import UserNotFoundError


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)


    def get_user_by_id(self, user_id: UUID) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError("User not found.")

        return user

    
    def update_user(self, data: UserUpdate, user_id: UUID) -> User:

        user = self.get_user_by_id(user_id)

        # Only include fields provided in the request
        update_data = data.model_dump(exclude_unset=True)

        # Hash password before saving
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        # Update model attributes dynamically
        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            self.db.commit()
            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise
    

    def delete_user(self, user_id: UUID) -> None:

        user = self.get_user_by_id(user_id)

        try:
            self.user_repository.delete(user)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
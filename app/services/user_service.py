from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.models.user import User


class UserService:

    def __init__(self, db):
        self.user_repository = UserRepository(db)

    def create_user(self, data):

        if self.get_user_by_email(data.email):
            raise ValueError("User with this email already exists.")
        
        hashed_password = hash_password(data.password)
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            mobile=data.mobile,
            email=data.email,
            password=hashed_password,
            date_of_birth=data.date_of_birth,
        )

        return self.user_repository.create(user)
    
    def get_user_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repository.get_by_email(email)
    
    def delete_user(self, data):
        user = self.get_user_by_email(data.email)
        if not user:
            raise ValueError("User not found.")
        
        return self.user_repository.delete(user)
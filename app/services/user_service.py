from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.core.auth import generate_token, verify_token
from app.models.user import User


class UserService:

    def __init__(self, db):
        self.user_repository = UserRepository(db)


    def create_user(self, data):

        if self.user_repository.get_by_email(data.email):
            raise HTTPException(
                status_code=401,
                detail="User with this email already exists."
                )
        
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
    

    def login_user(self, data):
        user = self.get_user_by_email(data.email)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email"
                )
        
        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid password"
                )
        
        access_token = generate_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    

    def update_user(self, data):
        user = self.get_user_by_id(data.email)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email"
                )
        
        hashed_password = hash_password(data.password)
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.mobile = data.mobile
        user.password = hashed_password
        user.date_of_birth = data.date_of_birth

        return self.user_repository.update(user)


    def get_user_by_id(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email"
                )
        return user
    

    def get_user_by_email(self, email):
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email"
                )
        return user
    

    def delete_user(self, user_id):        
        return self.user_repository.delete(user_id)
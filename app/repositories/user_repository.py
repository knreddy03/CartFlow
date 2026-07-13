from sqlalchemy import select
from app.models.user import User


class UserRepository:

    def __init__(self, db):
        self.db = db

    def create(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id):
        return self.db.get(User, user_id)

    def get_by_email(self, email):
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)
    
    def delete(self, user):
        return self.db.delete(user)
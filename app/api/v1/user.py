from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        data (UserCreate): The user registration data.
        db (Session): The database session.

    Returns:
        UserResponse: The registered user data.
    """

    try:
        user_service = UserService(db)
        user = user_service.create_user(data)
        return user
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

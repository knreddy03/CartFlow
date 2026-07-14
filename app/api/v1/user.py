from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.session import engine
from app.db.base import Base
from app.core.dependencies import get_current_user


Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
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


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Login an existing user.

    Args:
        data (UserLogin): The user login data.
        db (Session): The database session.

    Returns:
        The JWT token.
    """

    try:
        user_service = UserService(db)
        token = user_service.login_user(data)
        return token
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/profile")
def get_profile(current_user= Depends(get_current_user)):
    return current_user
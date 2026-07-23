from fastapi import APIRouter, Depends, status
from app.db.base import Base
from app.db.session import engine
from app.dependencies.service import get_user_service
from app.dependencies.user import get_current_user_id
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Register a new user.
    """

    return user_service.create_user(data)


@router.post(
    "/login",
)
def login(
    data: UserLogin,
    user_service: UserService = Depends(get_user_service),
):
    """
    Authenticate user and return access token.
    """

    return user_service.login_user(data)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_profile(
    user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
):
    """
    Get currently authenticated user's profile.
    """

    return user_service.get_user_by_id(user_id)


@router.patch(
    "/me",
    response_model=UserResponse,
)
def update_profile(
    data: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
):
    """
    Update currently authenticated user's profile.
    """

    return user_service.update_user(
        data,
        user_id,
    )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_profile(
    user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
):
    """
    Delete currently authenticated user's profile.
    """

    user_service.delete_user(user_id)
from fastapi import APIRouter, Depends, status
from app.dependencies.service import get_auth_service
from app.schemas.user_schema import UserResponse
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Register a new user.
    """

    return auth_service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Authenticate user and return access token.
    """

    return auth_service.login(data)
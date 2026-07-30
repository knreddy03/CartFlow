from fastapi import APIRouter, Depends, status
from app.dependencies.service import get_auth_service
from app.schemas.user_schema import UserResponse
from app.schemas.email_verification_schema import VerifyEmailRequest
from app.schemas.auth_schema import (
    RegisterRequest, 
    LoginRequest,
    RefreshTokenRequest, 
    TokenResponse
)
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


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Issue a new access token and rotate the refresh token.
    """

    return auth_service.refresh(data)


@router.post(
    "/verify-email",
    status_code=status.HTTP_200_OK,
)
def verify_email(
    data: VerifyEmailRequest,
    auth_service: AuthService = Depends(
        get_auth_service
    ),
):
    """
    Verify user's email address.
    """

    auth_service.verify_email(
        data.token
    )

    return {
        "message": "Email verified successfully."
    }


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Logout user.
    """

    auth_service.logout(data)
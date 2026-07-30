from datetime import datetime, timezone
import token
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.auth import create_access_token, create_refresh_token
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.exceptions.auth_exceptions import InvalidRefreshTokenError


class RefreshTokenService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = RefreshTokenRepository(db)


    def create_token(self, user_id: UUID) -> str:
        """
        Create JWT refresh token and store it.
        """

        token, expires_at = create_refresh_token(user_id)

        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )

        self.repository.add(refresh_token)

        return token


    def validate_token(self, token: str) -> RefreshToken:
        """
        Validate refresh token from database.
        """

        refresh_token = self.repository.get_by_token(token)

        if refresh_token is None:
            raise InvalidRefreshTokenError(
            "Invalid refresh token."
        )


        if refresh_token.revoked:
            raise InvalidRefreshTokenError(
            "Refresh token has been revoked."
        )


        if refresh_token.expires_at < datetime.now(timezone.utc):
            raise InvalidRefreshTokenError(
            "Refresh token has expired."
        )


        return refresh_token


    def rotate_token(self, token: str) -> tuple[str, str]:
        """
        Rotate refresh token and issue new token pair.
        """

        refresh_token = self.validate_token(token)

        self.repository.revoke(refresh_token)

        access_token = create_access_token(refresh_token.user_id)

        new_refresh_token = self.create_token(refresh_token.user_id)

        return (access_token, new_refresh_token)

    
    def revoke_token(self, token: str) -> None:
        """
        Revoke a refresh token.
        """

        refresh_token = self.validate_token(token)

        self.repository.revoke(refresh_token)
        

    def revoke_all_user_tokens(self, user_id: UUID) -> None:
        """
        Logout user from all devices.
        """

        self.repository.revoke_all_by_user(user_id)
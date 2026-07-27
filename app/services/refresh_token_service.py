from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.auth import create_refresh_token
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository


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

        try:
            self.repository.add(refresh_token)

            self.db.commit()
            self.db.refresh(refresh_token)

            return token

        except Exception:
            self.db.rollback()
            raise


    def validate_token(self, token: str) -> RefreshToken | None:
        """
        Validate refresh token from database.
        """

        refresh_token = self.repository.get_by_token(token)

        if refresh_token is None:
            return None


        if refresh_token.revoked:
            return None


        if refresh_token.expires_at < datetime.now(timezone.utc):
            return None


        return refresh_token


    def revoke_token(self, token: str) -> None:
        """
        Revoke a refresh token.
        """

        refresh_token = self.repository.get_by_token(token)

        if refresh_token:
            self.repository.revoke(refresh_token)

            self.db.commit()


    def revoke_all_user_tokens(self, user_id: UUID) -> None:
        """
        Logout user from all devices.
        """

        self.repository.revoke_all_by_user(user_id)

        self.db.commit()
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.auth import create_email_verification_token
from app.models.email_verification_token import EmailVerificationToken
from app.repositories.email_verification_repository import (
    EmailVerificationRepository,
)
from app.repositories.user_repository import UserRepository
from app.exceptions.email_verification_exceptions import (
    InvalidVerificationTokenError,
    VerificationTokenExpiredError,
    EmailAlreadyVerifiedError,
)


class EmailVerificationService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = EmailVerificationRepository(db)
        self.user_repository = UserRepository(db)


    def create_token(self, user_id: UUID,) -> str:
        """
        Create email verification token and persist it.
        """

        token, expires_at = create_email_verification_token(
            user_id
        )

        verification_token = EmailVerificationToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )

        self.repository.add(
            verification_token
        )

        return token


    def validate_token(self, token: str,) -> EmailVerificationToken:
        """
        Validate verification token.
        """

        verification_token = (
            self.repository.get_by_token(token)
        )

        if verification_token is None:
            raise InvalidVerificationTokenError(
                "Invalid verification token."
            )

        if verification_token.used:
            raise InvalidVerificationTokenError(
                "Verification token already used."
            )

        if verification_token.expires_at < datetime.now(timezone.utc):
            raise VerificationTokenExpiredError(
                "Verification token expired."
            )

        return verification_token


    def verify_email(self, token: str,) -> None:
        """
        Verify user's email address.
        """

        verification_token = self.validate_token(token)

        user = self.user_repository.get_by_id(
            verification_token.user_id
        )

        if user is None:
            raise InvalidVerificationTokenError(
                "User not found."
            )

        if user.is_verified:
            raise EmailAlreadyVerifiedError(
                "Email already verified."
            )

        user.is_verified = True

        self.repository.mark_used(
            verification_token
        )
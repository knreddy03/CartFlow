from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.email_verification_token import EmailVerificationToken
from uuid import UUID

class EmailVerificationRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, verification_token: EmailVerificationToken) -> None:
        self.db.add(verification_token)

    def get_by_token(self, token: str) -> EmailVerificationToken | None:
        stmt = select(EmailVerificationToken).where(EmailVerificationToken.token == token)
        return self.db.scalar(stmt)

    def get_by_id(self, token_id: UUID) -> EmailVerificationToken | None:
        return self.db.get(EmailVerificationToken, token_id)

    def mark_used(self,verification_token: EmailVerificationToken) -> None:
        verification_token.used = True

    def delete(self, verification_token: EmailVerificationToken) -> None:
        self.db.delete(verification_token)

    def delete_expired(self) -> None:
        pass
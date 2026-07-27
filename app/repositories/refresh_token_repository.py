from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from uuid import UUID

class RefreshTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, refresh_token: RefreshToken) -> None:
        self.db.add(refresh_token)

    def get_by_token(self, token: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        return self.db.scalar(stmt)

    def get_by_id(self, token_id: UUID) -> RefreshToken | None:
        return self.db.get(RefreshToken, token_id)

    def revoke(self,refresh_token: RefreshToken) -> None:
        refresh_token.revoked = True

    def revoke_all_by_user(self, user_id: UUID) -> None:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked.is_(False),
        )
        tokens = self.db.scalars(stmt).all()
        for token in tokens:
            token.revoked = True

    def delete(self, refresh_token: RefreshToken) -> None:
        self.db.delete(refresh_token)

    def delete_expired(self) -> None:
        pass
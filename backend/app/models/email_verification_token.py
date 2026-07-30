from sqlalchemy import Boolean, ForeignKey, DateTime, String
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_model import BaseModel
from uuid import UUID


class EmailVerificationToken(BaseModel):
    __tablename__ = "email_verification_tokens"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
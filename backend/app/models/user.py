from sqlalchemy import Enum as SQLEnum, String, Date, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_model import BaseModel
from enum import Enum
from datetime import date


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(BaseModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    mobile: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="user_role"), default=UserRole.CUSTOMER, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    cart = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan",)
    
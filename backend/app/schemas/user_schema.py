from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import UserRole
from datetime import date
from uuid import UUID


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    mobile: str
    email: EmailStr
    date_of_birth: date
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1)
    last_name: str | None = Field(default=None, min_length=1)
    mobile: str | None = Field(default=None, min_length=10, max_length=15)
    password: str | None = None
    date_of_birth: date | None = None
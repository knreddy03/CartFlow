from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    mobile: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    password: str
    date_of_birth: date


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    mobile: str
    email: EmailStr
    date_of_birth: date

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    mobile: str = Field(..., min_length=10, max_length=15)
    password: str
    date_of_birth: date
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    mobile: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    password: str
    date_of_birth: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD format


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    mobile: str
    email: EmailStr
    date_of_birth: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

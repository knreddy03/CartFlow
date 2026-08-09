from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    image_url: str = Field(..., max_length=255,)
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    slug: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    image_url: str = Field(..., max_length=255,)
    is_active: bool | None = None

class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
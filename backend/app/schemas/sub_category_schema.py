from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID


class SubCategoryBase(BaseModel):
    category_id: UUID = Field(..., description="The ID of the parent category",)
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    image_url: str | None = Field(default=None, max_length=255,)
    is_active: bool = True


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(BaseModel):
    category_id: UUID | None = Field(default=None, description="The ID of the parent category",)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    slug: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    image_url: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class SubCategoryResponse(SubCategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
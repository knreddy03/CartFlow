from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.dependencies.service import get_category_service
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Create a new category.
    """
    return category_service.create_category(category_data)


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories(
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Get all categories.
    """
    return category_service.get_all_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: UUID,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Get category by ID.
    """
    return category_service.get_category_by_id(category_id)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Update a category.
    """
    return category_service.update_category(category_id, category_data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: UUID,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Delete a category.
    """
    category_service.delete_category(category_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
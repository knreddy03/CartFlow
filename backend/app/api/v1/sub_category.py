from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.dependencies.service import get_sub_category_service
from app.schemas.sub_category_schema import (
    SubCategoryCreate,
    SubCategoryResponse,
    SubCategoryUpdate,
)
from app.services.sub_category_service import SubCategoryService


router = APIRouter(
    prefix="/sub-categories",
    tags=["Sub Categories"],
)


@router.post(
    "",
    response_model=SubCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sub_category(
    sub_category_data: SubCategoryCreate,
    sub_category_service: SubCategoryService = Depends(
        get_sub_category_service
    ),
):
    """
    Create a new sub-category.
    """
    return sub_category_service.create_sub_category(
        sub_category_data
    )


@router.get(
    "",
    response_model=list[SubCategoryResponse],
)
def get_sub_categories(
    sub_category_service: SubCategoryService = Depends(
        get_sub_category_service
    ),
):
    """
    Get all sub-categories.
    """
    return sub_category_service.get_all_sub_categories()


@router.get(
    "/category/{category_id}",
    response_model=list[SubCategoryResponse],
)
def get_sub_categories_by_category(
    category_id: UUID,
    sub_category_service: SubCategoryService = Depends(
        get_sub_category_service
    ),
):
    """
    Get all sub-categories belonging to a category.
    """
    return sub_category_service.get_sub_categories_by_category(
        category_id
    )


@router.get(
    "/{sub_category_id}",
    response_model=SubCategoryResponse,
)
def get_sub_category(
    sub_category_id: UUID,
    sub_category_service: SubCategoryService = Depends(
        get_sub_category_service
    ),
):
    """
    Get a sub-category by ID.
    """
    return sub_category_service.get_sub_category_by_id(
        sub_category_id
    )


@router.patch(
    "/{sub_category_id}",
    response_model=SubCategoryResponse,
)
def update_sub_category(
    sub_category_id: UUID,
    sub_category_data: SubCategoryUpdate,
    sub_category_service: SubCategoryService = Depends(
        get_sub_category_service
    ),
):
    """
    Update a sub-category.
    """
    return sub_category_service.update_sub_category(
        sub_category_id,
        sub_category_data,
    )


@router.delete(
    "/{sub_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_sub_category(
    sub_category_id: UUID,
    sub_category_service: SubCategoryService = Depends(
        get_sub_category_service
    ),
):
    """
    Delete a sub-category.
    """
    sub_category_service.delete_sub_category(
        sub_category_id
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
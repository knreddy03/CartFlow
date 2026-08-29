from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from app.dependencies.user import require_admin
from app.dependencies.service import get_product_service
from app.schemas.product_schema import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService
from app.models.user import User


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_product(
    product_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
):
    """
    Create a new product.
    """
    return product_service.create_product(product_data)


@router.get(
    "",
    response_model=ProductListResponse,
)
def get_products(
    category_id: UUID | None = Query(
        default=None,
        description="Filter products by category ID",
    ),
    sub_category_id: UUID | None = Query(
        default=None,
        description="Filter products by sub-category ID",
    ),
    is_active: bool | None = Query(
        default=None,
        description="Filter products by active status",
    ),
    min_price: int | None = Query(
        default=None,
        ge=0,
        description="Minimum product price in cents",
    ),
    max_price: int | None = Query(
        default=None,
        ge=0,
        description="Maximum product price in cents",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of products per page",
    ),
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get products with optional filtering and pagination.
    """
    return product_service.get_products(
        category_id=category_id,
        sub_category_id=sub_category_id,
        is_active=is_active,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get product by ID.
    """
    return product_service.get_product_by_id(product_id)


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
     _: User = Depends(require_admin),
):
    """
    Update a product.
    """
    return product_service.update_product(product_id, product_data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service),
    _: User = Depends(require_admin),
):
    """
    Delete a product.
    """
    product_service.delete_product(product_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
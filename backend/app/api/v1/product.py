from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.dependencies.service import get_product_service
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
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
    response_model=list[ProductResponse],
)
def get_products(
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get all products.
    """
    return product_service.get_all_products()


@router.get(
    "/category/{category_id}",
    response_model=list[ProductResponse],
)
def get_products_by_category(
    category_id: UUID,
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get products by category.
    """
    return product_service.get_products_by_category(category_id)


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
):
    """
    Delete a product.
    """
    product_service.delete_product(product_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
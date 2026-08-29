from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.dependencies.user import require_admin
from app.dependencies.service import get_product_variant_service
from app.schemas.product_variant_schema import (
    ProductVariantCreate,
    ProductVariantResponse,
    ProductVariantUpdate,
)
from app.services.product_variant_service import ProductVariantService


router = APIRouter(
    prefix="/products/{product_id}/variants",
    tags=["Product Variants"],
)


@router.post(
    "",
    response_model=ProductVariantResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_product_variant(
    product_id: UUID,
    variant_data: ProductVariantCreate,
    product_variant_service: ProductVariantService = Depends(
        get_product_variant_service
    ),
):
    """
    Create a variant for a product.
    """
    return product_variant_service.create_product_variant(
        product_id,
        variant_data,
    )


@router.get(
    "",
    response_model=list[ProductVariantResponse],
)
def get_product_variants(
    product_id: UUID,
    product_variant_service: ProductVariantService = Depends(
        get_product_variant_service
    ),
):
    """
    Get all variants for a product.
    """
    return product_variant_service.get_product_variants(
        product_id
    )


@router.get(
    "/{variant_id}",
    response_model=ProductVariantResponse,
)
def get_product_variant(
    product_id: UUID,
    variant_id: UUID,
    product_variant_service: ProductVariantService = Depends(
        get_product_variant_service
    ),
):
    """
    Get a product variant by ID.
    """
    return product_variant_service.get_product_variant_by_id(
        product_id,
        variant_id,
    )


@router.patch(
    "/{variant_id}",
    response_model=ProductVariantResponse,
    dependencies=[Depends(require_admin)],
)
def update_product_variant(
    product_id: UUID,
    variant_id: UUID,
    variant_data: ProductVariantUpdate,
    product_variant_service: ProductVariantService = Depends(
        get_product_variant_service
    ),
):
    """
    Update a product variant.
    """
    return product_variant_service.update_product_variant(
        product_id,
        variant_id,
        variant_data,
    )


@router.delete(
    "/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_product_variant(
    product_id: UUID,
    variant_id: UUID,
    product_variant_service: ProductVariantService = Depends(
        get_product_variant_service
    ),
):
    """
    Delete a product variant.
    """
    product_variant_service.delete_product_variant(
        product_id,
        variant_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.dependencies.service import get_cart_service
from app.dependencies.user import get_current_user_id
from app.schemas.cart_schema import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
)
from app.services.cart_service import CartService


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.get(
    "",
    response_model=CartResponse,
)
def get_cart(
    user_id: UUID = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    """
    Get the authenticated user's cart.
    """
    return cart_service.get_cart(user_id)


@router.post(
    "/items",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_cart_item(
    item_data: CartItemCreate,
    user_id: UUID = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    """
    Add a product to the authenticated user's cart.
    """
    return cart_service.add_item(
        user_id,
        item_data,
    )


@router.patch(
    "/items/{cart_item_id}",
    response_model=CartItemResponse,
)
def update_cart_item(
    cart_item_id: UUID,
    item_data: CartItemUpdate,
    user_id: UUID = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    """
    Update the quantity of an item in the authenticated user's cart.
    """
    return cart_service.update_item(
        user_id,
        cart_item_id,
        item_data,
    )


@router.delete(
    "/items/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_cart_item(
    cart_item_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    cart_service: CartService = Depends(get_cart_service),
):
    """
    Remove an item from the authenticated user's cart.
    """
    cart_service.remove_item(
        user_id,
        cart_item_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
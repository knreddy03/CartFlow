from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User

from app.dependencies.service import get_order_service
from app.dependencies.user import get_current_user_id, require_admin
from app.exceptions.cart_exceptions import (
    CartEmptyError,
    CartNotFoundError,
    InsufficientStockError,
    ProductOutOfStockError,
)
from app.exceptions.order_exceptions import (
    InvalidOrderStatusTransitionError,
    OrderNotFoundError,
)
from app.exceptions.product_exceptions import ProductNotFoundError
from app.exceptions.product_variant_exceptions import (
    ProductVariantNotFoundError,
)
from app.schemas.order_schema import OrderResponse, OrderStatusUpdate
from app.services.order_service import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    user_id: UUID = Depends(get_current_user_id),
    order_service: OrderService = Depends(get_order_service),
):
    try:
        return order_service.create_order(user_id)

    except CartNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except CartEmptyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ProductVariantNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ProductOutOfStockError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except InsufficientStockError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[OrderResponse],
)
def get_orders(
    user_id: UUID = Depends(get_current_user_id),
    order_service: OrderService = Depends(get_order_service),
):
    return order_service.get_user_orders(user_id)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    order_service: OrderService = Depends(get_order_service),
):
    try:
        return order_service.get_order(
            order_id=order_id,
            user_id=user_id,
        )

    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
def update_order_status(
    order_id: UUID,
    payload: OrderStatusUpdate,
    _: User = Depends(require_admin),
    order_service: OrderService = Depends(get_order_service),
):
    try:
        return order_service.update_order_status(
            order_id=order_id,
            new_status=payload.status,
        )

    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except InvalidOrderStatusTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{order_id}/cancel",
    response_model=OrderResponse,
)
def cancel_order(
    order_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    order_service: OrderService = Depends(get_order_service),
):
    try:
        return order_service.cancel_order(
            order_id=order_id,
            user_id=user_id,
        )

    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except InvalidOrderStatusTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
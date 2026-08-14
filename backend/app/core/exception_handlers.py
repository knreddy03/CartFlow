from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidCredentialsError,
)

from app.exceptions.category_exceptions import (
    CategoryNotFoundError,
    CategoryAlreadyExistsError,
)

from app.exceptions.product_exceptions import (
    ProductNotFoundError,
    ProductAlreadyExistsError,
)

from app.exceptions.cart_exceptions import (
    CartNotFoundError,
    CartItemNotFoundError,
    ProductOutOfStockError,
    InsufficientStockError,
)


def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        },
    )


def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )


def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": str(exc)
        },
    )


def category_not_found_handler(
    request: Request,
    exc: CategoryNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )


def category_already_exists_handler(
    request: Request,
    exc: CategoryAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        },
    )


def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )


def product_already_exists_handler(
    request: Request,
    exc: ProductAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        },
    )


def cart_not_found_handler(
    request: Request,
    exc: CartNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )


def cart_item_not_found_handler(
    request: Request,
    exc: CartItemNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )


def product_out_of_stock_handler(
    request: Request,
    exc: ProductOutOfStockError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        },
    )


def insufficient_stock_handler(
    request: Request,
    exc: InsufficientStockError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        },
    )

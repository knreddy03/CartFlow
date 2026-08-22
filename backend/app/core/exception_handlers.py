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

from app.exceptions.sub_category_exceptions import (
    SubCategoryNotFoundError,
    SubCategoryAlreadyExistsError,
)

from app.exceptions.product_exceptions import (
    ProductNotFoundError,
    ProductAlreadyExistsError,
    MinPriceGreaterThanMaxPriceError,
)

from app.exceptions.product_variant_exceptions import (
    ProductVariantNotFoundError,
    ProductVariantAlreadyExistsError,
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


def sub_category_not_found_handler(
    request: Request,
    exc: SubCategoryNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )


def sub_category_already_exists_handler(
    request: Request,
    exc: SubCategoryAlreadyExistsError,
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


def product_variant_not_found_handler(
    request: Request,
    exc: ProductVariantNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )


def product_variant_already_exists_handler(
    request: Request,
    exc: ProductVariantAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        },
    )


def min_price_greater_than_max_price_handler(
    request: Request,
    exc: MinPriceGreaterThanMaxPriceError,
):
    return JSONResponse(
        status_code=400,
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

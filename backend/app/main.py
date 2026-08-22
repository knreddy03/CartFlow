from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.user import router as user_router
from app.api.v1.auth import router as auth_router
from app.api.v1.category import router as category_router
from app.api.v1.sub_category import router as sub_category_router
from app.api.v1.product import router as product_router
from app.api.v1.product_variant import router as product_variant_router
from app.api.v1.cart import router as cart_router

from app.core.exception_handlers import (
    user_already_exists_handler,
    user_not_found_handler,
    invalid_credentials_handler,
    category_not_found_handler,
    category_already_exists_handler,
    sub_category_already_exists_handler,
    sub_category_not_found_handler,
    product_not_found_handler,
    product_already_exists_handler,
    min_price_greater_than_max_price_handler,
    product_variant_not_found_handler,
    product_variant_already_exists_handler,
    cart_not_found_handler,
    cart_item_not_found_handler,
    product_out_of_stock_handler,
    insufficient_stock_handler,
)

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


app = FastAPI(
    title="Cart Flow",
    description="API for managing cart flow operations",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler,
)

app.add_exception_handler(
    UserNotFoundError,
    user_not_found_handler,
)

app.add_exception_handler(
    InvalidCredentialsError,
    invalid_credentials_handler,
)

app.add_exception_handler(
    CategoryNotFoundError,
    category_not_found_handler,
)

app.add_exception_handler(
    CategoryAlreadyExistsError,
    category_already_exists_handler,
)

app.add_exception_handler(
    SubCategoryNotFoundError,
    sub_category_not_found_handler,
)

app.add_exception_handler(
    SubCategoryAlreadyExistsError,
    sub_category_already_exists_handler,
)

app.add_exception_handler(
    ProductNotFoundError,
    product_not_found_handler,
)

app.add_exception_handler(
    ProductAlreadyExistsError,
    product_already_exists_handler,
)

app.add_exception_handler(
    MinPriceGreaterThanMaxPriceError,
    min_price_greater_than_max_price_handler,
)

app.add_exception_handler(
    ProductVariantNotFoundError,
    product_variant_not_found_handler,
)

app.add_exception_handler(
    ProductVariantAlreadyExistsError,
    product_variant_already_exists_handler,
)

app.add_exception_handler(
    CartNotFoundError,
    cart_not_found_handler,
)

app.add_exception_handler(
    CartItemNotFoundError,
    cart_item_not_found_handler,
)

app.add_exception_handler(
    ProductOutOfStockError,
    product_out_of_stock_handler,
)

app.add_exception_handler(
    InsufficientStockError,
    insufficient_stock_handler,
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(sub_category_router)
app.include_router(product_router)
app.include_router(product_variant_router)
app.include_router(cart_router)


@app.get("/")
def root():
    return {"message": "Welcome to Cart Flow API!"}

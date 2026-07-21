from fastapi import FastAPI
from app.api.v1.user import router as user_router

from app.core.exception_handlers import (
    user_already_exists_handler,
    user_not_found_handler,
    invalid_credentials_handler,
)

from app.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidCredentialsError,
)


app = FastAPI(
    title="Cart Flow",
    description="API for managing cart flow operations",
    version="1.0.0",
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

app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Welcome to Cart Flow API!"}

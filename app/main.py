from fastapi import FastAPI
import uvicorn
from app.api.v1.user import router as user_router

app = FastAPI(
    title="Cart Flow",
    description="API for managing cart flow operations",
    version="1.0.0",
)

app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Welcome to Cart Flow API!"}

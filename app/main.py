from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Cart Flow",
    description="API for managing cart flow operations",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to Cart Flow API!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

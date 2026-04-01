from fastapi import FastAPI
from app.api.v1.endpoints import product


app = FastAPI(title="Price Tracker")


app.include_router(product.router, prefix="/api/products", tags=["products"])


@app.get("/")
def root():
    return {"message": "API is running"}
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import close_db
from app.utils.cache import close_cache

from app.routers import product

from app.core.config import settings



@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting application")

    yield

    print("Stopping application")

    await close_cache()
    await close_db()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)


app.include_router(
    product.router,
    prefix="/api/products",
    tags=[
        "products"
    ],
)


@app.get("/")
def root():
    return {"message": "API is running"}
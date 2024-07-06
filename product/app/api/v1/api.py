from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.routes import product


api_router = APIRouter()


api_router.include_router(product.router, prefix="/product", tags=["product"])


@api_router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
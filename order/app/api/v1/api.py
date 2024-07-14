from fastapi import APIRouter
from app.api.v1.routes.order import router as order_router


APIRouter = APIRouter()


APIRouter.include_router(order_router, prefix="/order")


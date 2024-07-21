from fastapi import APIRouter
from app.api.v1.routes.order import router as order_router
from app.api.dep import GetCurrentAdminDep,LoginForAccessTokenDep

APIRouter = APIRouter()


APIRouter.include_router(order_router, prefix="/order")


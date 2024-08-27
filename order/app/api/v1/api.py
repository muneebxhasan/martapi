from fastapi import APIRouter
from app.api.v1.routes.order import router as order_router
from app.api.v1.routes.order_admin import router as order_admin_router
from app.api.dep import GetCurrentAdminDep

APIRouter = APIRouter()


APIRouter.include_router(order_router, prefix="/order",tags=["order"])


APIRouter.include_router(order_admin_router, prefix="/admin", dependencies=[GetCurrentAdminDep],tags=["order_admin"])



# APIRouter.include_router(order_router, prefix="/order", dependencies=[GetCurrentAdminDep])

# APIRouter.include_router(order_router, prefix="/order", dependencies=[GetCurrentUserDep])


from fastapi import APIRouter
from app.api.routes.v1.inventory import router as inventory_router
from app.api.deps import GetCurrentAdminDep
api_router = APIRouter()

# api_router.include_router(inventory_router, prefix="/inventory")

api_router.include_router(inventory_router, prefix="/inventory", dependencies=[GetCurrentAdminDep])
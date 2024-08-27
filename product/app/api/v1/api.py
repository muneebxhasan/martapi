from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.routes.product import router as product_router # import router
from app.api.v1.routes.product_admin import router as product_admin_router # import router
from app.api.dep import GetCurrentAdminDep

api_router = APIRouter()


api_router.include_router(product_router,  tags=["product"])
api_router.include_router(product_admin_router, prefix="/admin", tags=["product_admin"],dependencies=[GetCurrentAdminDep])


@api_router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
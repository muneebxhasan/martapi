from fastapi import APIRouter
from app.api.v1.routes.user import router
from app.api.v1.routes.login import router as login_router

app_router = APIRouter()

app_router.include_router(login_router, tags=["login"])
app_router.include_router(router, prefix="/user", tags=["user"])
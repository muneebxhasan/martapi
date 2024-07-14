from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.core import db_eng
from app import setting
# from fastapi.openapi.docs import get_swagger_ui_html
from app.api.v1.api import APIRouter

def create_db_and_tables():
    print("Creating tables...")
    SQLModel.metadata.create_all(db_eng.engine)


@asynccontextmanager
async def lifespan(app: FastAPI)->AsyncGenerator[None, None]:
    print("Life Span...")

    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="order api", version="0.0.1",
            servers=[{
                "url": "http://127.0.0.1:8003", # ADD NGROK URL Here Before Creating GPT Action
                "description": "Development Server"
            }] 
            )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(APIRouter, prefix=setting.API_STRING)

@app.get("/")
def redirect_to_root():
    return RedirectResponse(url="/docs")

# @app.get("/docss", include_in_schema=False)
# async def custom_swagger_ui_html_cdn():
#     return get_swagger_ui_html(
#     openapi_url="openapi.json",
#     title=f"{app.title} - Swagger UI",
#     # swagger_ui_dark.css CDN link
#     swagger_css_url="https://github.com/oqo0/swagger-themes/blob/main/SwaggerThemes/Themes/universal-dark.css"
# )

@app.get(f"{setting.API_STRING}/container", tags=["Health"])
def read_root():
    return {"Container": "Product services", "Port": "8003"}
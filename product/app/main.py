# main.py
from contextlib import asynccontextmanager
from app import settings
from fastapi.responses import RedirectResponse
from sqlmodel import  SQLModel
from fastapi import  FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer
import asyncio
import json
from app.api.v1 import api as api_v1
from app.core import db_eng
from app.api.dep import LoginForAccessTokenDep






def create_db_and_tables()->None:
    SQLModel.metadata.create_all(db_eng.engine)



@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
   
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="product api", 
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_v1.api_router,prefix=settings.API_STRING)



@app.get("/")
async def redirect_to_docs():
    
    return RedirectResponse(url="/docs")



@app.get(f"{settings.API_STRING}/container", tags=["Health"])
def read_root():
    return {"Container": "Product services", "Port": "8000"}


@app.post("/auth/login", tags=["Wrapper Auth"])
def login_for_access_token(form_data: LoginForAccessTokenDep):
    return form_data

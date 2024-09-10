# main.py
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaConsumer
from app.consumer.order_consummer import update_stock_messages
from app.consumer.product_consumer import add_stock_messages
from fastapi import FastAPI
from typing import AsyncGenerator
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.api import api_router as api_V1
import asyncio
from app.api.deps import LoginForAccessTokenDep
from app.core import db_eng
from app.settings import BOOTSTRAP_SERVER,KAFKA_ORDER_TOPIC,KAFKA_PRODUCT_TOPIC 
from sqlmodel import SQLModel

# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
loop = asyncio.get_event_loop()
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Starting app..")
  
    asyncio.create_task(add_stock_messages('add_stock', BOOTSTRAP_SERVER))   
    asyncio.create_task(update_stock_messages('update_stock', BOOTSTRAP_SERVER))


    create_db_and_tables()
    yield

def create_db_and_tables()->None:
    SQLModel.metadata.create_all(db_eng.engine)
    
app = FastAPI(lifespan=lifespan, title="Inventroy Service", 
            root_path="/inventory-service",root_path_in_servers=True,
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8086", # ADD NGROK URL Here Before Creating GPT Action
            
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
app.include_router(api_V1, prefix="/v1/inventory_service")

@app.get("/")
def read_root():


    return {"App": "Service 2"}


@app.post("/auth/login", tags=["Wrapper Auth"])
def login_for_access_token(form_data: LoginForAccessTokenDep):
    return form_data


# main.py
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaConsumer
from app.consumer.product_consumer import consume_messages
from fastapi import FastAPI
from typing import AsyncGenerator
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.api import api_router as api_V1
import asyncio
from app.core import db_eng
import json
from sqlmodel import SQLModel

# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
loop = asyncio.get_event_loop()
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    asyncio.create_task(consume_messages('todos', 'broker:19092'))    

    create_db_and_tables()
    yield

def create_db_and_tables()->None:
    SQLModel.metadata.create_all(db_eng.engine)
    
app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8002", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        },{
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
app.include_router(api_V1, prefix="/v1/inventory_service")

@app.get("/")
def read_root():


    return {"App": "Service 2"}

# # Kafka Producer as a dependency
# async def get_kafka_producer():
#     producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
#     await producer.start()
#     try:
#         yield producer
#     finally:
#         await producer.stop()
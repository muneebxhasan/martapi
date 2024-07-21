from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.core import db_eng
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import setting
from app.api.v1.api import app_router
from app.consumer.notification_consumer import user_detail
from app.initial_data import main as init_db_main
import asyncio
from app.setting import BOOTSTRAP_SERVER

def create_db_and_tables():
    print("Creating tables...")
    SQLModel.metadata.create_all(db_eng.engine)

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    init_db_main()
    # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
    asyncio.create_task(user_detail("get_user", BOOTSTRAP_SERVER))
    # create_db_and_tables()

    yield
app = FastAPI(lifespan=lifespan, title="User api",servers=[{
                "url": "http://127.0.0.1:8004", # ADD NGROK URL Here Before Creating GPT Action
                "description": "Development Server"
            }] )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(app_router, prefix=setting.API_STRING)
@app.get("/")
def read_root():
    return {"Hello  User service": "port 8004"}
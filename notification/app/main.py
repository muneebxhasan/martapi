from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any
from sqlmodel import SQLModel
from app.core import db_eng
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.consumer.order_consumer import order_conformation_notification_message
from app.consumer.user_consumer import user_detail_messages
from app.setting import BOOTSTRAP_SERVER
from app.consumer.user_register import register_user_message

from app import setting
from app.send_notification import order_notifications


def create_db_and_tables():
    print("Creating tables...")
    SQLModel.metadata.create_all(db_eng.engine)

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    asyncio.create_task(register_user_message("user_notify",BOOTSTRAP_SERVER))
    asyncio.create_task(order_conformation_notification_message('order_conformation_notification', BOOTSTRAP_SERVER))
    asyncio.create_task(user_detail_messages('order_notification', BOOTSTRAP_SERVER))

    yield

app = FastAPI(lifespan=lifespan, title="notification api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    
    # user = requests.get_user()  #
    # return user
    return {"Hello notification serivce": "8005"}



@app.get('/send-email/asynchronous')
async def send_email_asynchronous():
    asyncio.create_task(order_notifications(setting.CILENT_ID, setting.CLIENT_SECRET,{
	"user": {
		"user_id": 1,
		"full_name": "muneeb",
		"email": "muneebxhasan@gmail.com",
		"number": 1234567890,
		"address": "paksitan"
	},
	"notification": {
		"order_id": 1,
		"user_id": 1,
		"notification_id": "order_confirmation"
	}
    }))
    
    return {"message": "Email sent successfully"}
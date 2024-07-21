from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any
from sqlmodel import SQLModel
from app.core import db_eng
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.consumer.order_consumer import notification_messages
from app.setting import BOOTSTRAP_SERVER
from app.consumer.user_register import register_user_message
from fastapi import BackgroundTasks
# from app.send_mail import send_email_async, send_email_background
from app.send_mail import generate_test_email,send_email

def create_db_and_tables():
    print("Creating tables...")
    SQLModel.metadata.create_all(db_eng.engine)

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    
    asyncio.create_task(register_user_message("user_notify",BOOTSTRAP_SERVER))
    asyncio.create_task(notification_messages('order_conformation', BOOTSTRAP_SERVER))
    # asyncio.create_task(notification_messages('user_details', BOOTSTRAP_SERVER))

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
    # await send_email_async('Hello World','muneebxhasan@gmail.com',
    # {'title': 'Hello World', 'name': 'John Doe'})
    x = generate_test_email("muneebxhasan@gmail.com")


    return x
@app.get('/send-email/backgroundtasks')
def send_email_backgroundtasks():
    # send_email_background(background_tasks, 'Hello World',   
    # 'muneebxhasan@gmail.com', {'title': 'Hello World', 'name':       'John Doe'})
    try:
        response = send_email("muneebxhasan@gmail.com", "Test Subject", "<h1>Test Email</h1>")
        print("Email sent successfully, response:", response)
        return response
    except Exception as e:
        print("Failed to send email:", str(e))
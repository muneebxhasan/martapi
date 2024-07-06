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
from app.core.dp_kafka import Producer

# class Todo(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     content: str = Field(index=True)


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
# connection_string = str(settings.DATABASE_URL).replace(
#     "postgresql", "postgresql+psycopg"
# )


# recycle connections after 5 minutes
# to correspond with the compute scale down
# engine = create_engine(
#     connection_string, connect_args={}, pool_recycle=300
# )

#engine = create_engine(
#    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
#)


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(db_eng.engine)



# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
# loop = asyncio.get_event_loop()
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
    # task = asyncio.create_task(consume_messages('todos', 'broker:19092'))
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
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

# async def get_kafka_producer():
#     producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
#     await producer.start()
#     try:
#         yield producer
#     finally:
#         await producer.stop()

# def get_session():
#     with Session(db_en.engine) as session:
#         yield session  


@app.get("/")
async def redirect_to_docs(producer:Producer):
    todo_json = json.dumps({
  "product_id": 4,
  "variant_id": 0,
  "quantity": 0,
  "id": 4
}).encode("utf-8")
    await producer.send_and_wait("todos", todo_json)
    return todo_json
    # return RedirectResponse(url="/docs")



@app.get(f"{settings.API_STRING}/container", tags=["Health"])
def read_root():
    return {"Container": "Product services", "Port": "8000"}

# Kafka Producer as a dependency

# @app.post("/todos/", response_model=Todo)
# async def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)])->Todo:
#         todo_dict = {field: getattr(todo, field) for field in todo.dict()}
#         todo_json = json.dumps(todo_dict).encode("utf-8")
#         print("todoJSON:", todo_json)
#         # Produce message
#         await producer.send_and_wait("todos", todo_json)
#         # session.add(todo)
#         # session.commit()
#         # session.refresh(todo)
#         return todo


# @app.get("/todos/", response_model=list[Todo])
# def read_todos(session: Annotated[Session, Depends(get_session)]):
#         todos = session.exec(select(Todo)).all()
#         return todos
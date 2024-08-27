from aiokafka import AIOKafkaConsumer
import json
from app.crud.order_crud import update_status
from app.core.db_eng import engine
from sqlmodel import Session

async def get_payment_status_update_consumer(topic:str,BOOTSTRAP_SERVER:str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP_SERVER,
        group_id='payment_status_update',
        
    )
    
    await consumer.start()
    try:
        async for msg in consumer:
            order_details = json.loads(msg.value.decode("utf-8")) # type: ignore
            with Session(engine) as db:
                id  = int(order_details.get("order_id"))
                update_status(id, "paid", db)


    finally:
        await consumer.stop()
    
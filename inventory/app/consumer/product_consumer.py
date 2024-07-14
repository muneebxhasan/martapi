from aiokafka import AIOKafkaConsumer
from sqlmodel import select
from app.core.deps import get_session
from app.crud.inventory_crud import add_new_inventoryItem
from app.model.inventory_model import Inventory
import json


async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="Stocks-Consumer-Group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}") # type: ignore

            inventory__data = json.loads(message.value.decode()) # type: ignore
            print("TYPE", (type(inventory__data)))
            print(f"Inventory Data {inventory__data}")

            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                db_insert_product = add_new_inventoryItem(
                        inventory_data=Inventory(**inventory__data), 
                        session=session)
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

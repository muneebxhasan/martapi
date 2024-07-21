from aiokafka import AIOKafkaConsumer
from app.core.deps import get_session
from app.crud.inventory_crud import update_stock_by_product_id
import json

async def update_stock_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="Stocks-Consumer-Group"
        # auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages. 
        async for message in consumer:
            # print(f"Received message: {message.value.decode()} on topic {message.topic}") # type: ignore

            inventory__data = json.loads(message.value.decode()) # type: ignore
            print("TYPE", (type(inventory__data)))
            print(f"Inventory Data {inventory__data}")

            with next(get_session()) as session:
                print("updating stock")
                update_stock_by_product_id(inventory__data['product_id'], inventory__data['option_id'], inventory__data['quantity'], session)
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
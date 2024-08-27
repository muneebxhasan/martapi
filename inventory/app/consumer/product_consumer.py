from aiokafka import AIOKafkaConsumer
from app.core.deps import get_session
from app.crud.inventory_crud import add_new_inventoryItem
from app.model.inventory_model import Inventory
import json
from app import stock_pb2
from google.protobuf.json_format import MessageToDict

async def add_stock_messages(topic, bootstrap_servers):
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

            # inventory__data = json.loads(message.value.decode()) # type: ignore
            # print("TYPE", (type(inventory__data)))
            # print(f"Inventory Data {inventory__data}")

            inventory__data = stock_pb2.Stock()
            inventory__data.ParseFromString(message.value)
            print("Inventory Data", inventory__data)
            
            inventory__data = MessageToDict(inventory__data,preserving_proto_field_name=True)
            print("Inventory Data", inventory__data)
            # Inventory.model_dump(inventory__data)
            inventory_item=Inventory(
                product_id=inventory__data["product_id"],
                option_id=inventory__data["option_id"],
                quantity=inventory__data["quantity"]
            )
            # print(inventory__data)
            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                db_insert_product = add_new_inventoryItem(
                        inventory_item,
                        session)
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

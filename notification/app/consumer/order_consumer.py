from aiokafka import AIOKafkaConsumer
from app.setting import KAFKA_GROUP_ID
import json
from app.consumer.get_user import get_user
from app.consumer.user_consumer import user_detail_messages
import asyncio
async def order_conformation_notification_message(topic: str, BOOTSTRAP_SERVER: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP_SERVER,
        group_id=KAFKA_GROUP_ID,
        session_timeout_ms=10000,  # Default is 10000 (10 seconds)
        max_poll_interval_ms=600000,
        
    )
    
    await consumer.start()
    try:
        async for msg in consumer:
            notification_detail = json.loads(msg.value.decode("utf-8")) # type: ignore
            print("----------------calling get_user----------------")
            print(f"Notification: {notification_detail}")
            await get_user(notification_detail)
     
    finally:
        await consumer.stop()

    

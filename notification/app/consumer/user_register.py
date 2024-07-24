from aiokafka import AIOKafkaConsumer
from app import setting
import json
import asyncio
from app.send_notification import user_notifications

async def register_user_message(topic:str,BOOTSTRAP_SERVER:str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP_SERVER,
        group_id=setting.KAFKA_GROUP_ID,
        session_timeout_ms=10000,  # Default is 10000 (10 seconds)
        max_poll_interval_ms=600000
    )

    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value.decode("utf-8")) # type: ignore
            asyncio.create_task(user_notifications(setting.CILENT_ID,setting.CLIENT_SECRET,message))
            print("/n/nuser/n/n",message)
    finally:
        await consumer.stop()
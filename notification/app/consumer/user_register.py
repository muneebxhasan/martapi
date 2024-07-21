from aiokafka import AIOKafkaConsumer
from app import setting
import json

async def register_user_message(topic:str,BOOTSTRAP_SERVER:str):
    consumer = AIOKafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        group_id=setting.KAFKA_GROUP_ID,
        session_timeout_ms=10000,  # Default is 10000 (10 seconds)
        max_poll_interval_ms=600000
    )

    await consumer.start()
    try:
        async for msg in consumer:
            notification = json.loads(msg.value.decode("utf-8")) # type: ignore
            if notification["event"] == "user_registered":
                pass
            elif notification["event"] == "user_updated":
                pass
            elif notification["event"] == "user_password_changed":
                pass
            print("/n/nuser/n/n",notification)
    finally:
        await consumer.stop()
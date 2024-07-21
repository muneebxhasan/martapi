from aiokafka import AIOKafkaConsumer
from app.send_notification import send_notification
from app import setting
import json

async def user_detail_messages(topic: str, BOOTSTRAP_SERVER: str,notification):
    print("User Details..")
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
            # print(f"User Details: {msg.value.decode('utf-8')}")  # type: ignore
            user = json.loads(msg.value.decode("utf-8")) # type: ignore
            if user["user_id"] == notification["user_id"]:
                await send_notification(setting.CILENT_ID, setting.CLIENT_SECRET,user,notification)

    finally:
        await consumer.stop()


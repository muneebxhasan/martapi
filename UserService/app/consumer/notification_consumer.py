from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from app.model.user_model import UserInfo
from app.crud.user_crud import get_user_by_id 
from app.api.deps import get_session

async def user_detail(topic: str, BOOTSTRAP_SERVER: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP_SERVER,
    )
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    await consumer.start()
    await producer.start()
    try:
        async for msg in consumer:
            user = json.loads(msg.value.decode("utf-8"))  # type: ignore
            user_id = int(user["user_id"])

            with next(get_session()) as db:
                user:UserInfo = get_user_by_id(user_id, db)
                user_ = {
                    "user_id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "number": "03123456789"
                }
                user_ = json.dumps(user_).encode("utf-8")
                await producer.send_and_wait("user_details", user_)


    finally:
        await producer.stop()
        await consumer.stop()
        



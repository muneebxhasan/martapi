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
            notification = json.loads(msg.value.decode("utf-8"))  # type: ignore
            user_id = notification.get("user_id")
            user_id = int(user_id)
            print("User ID:", user_id)
            print("Notification:", notification)

            with next(get_session()) as db:  
                user:UserInfo = get_user_by_id(user_id, db)
                if user is not None:
                    user_data = {
                        "user_id": user.id,
                        "full_name": user.full_name,
                        "email": user.email,
                        "number": user.number,
                        "address": user.address,
                    }

                    # Add order confirmation notification
                    order_notification = {
                        "order_id": notification.get("order_id"),
                        "user_id": user.id,
                        "notification_id": notification.get("notification_id")
                    }
                    # print("order_notification", order_notification)
                
                    message = {
                    "user": user_data,
                    "notification": order_notification
                    }
                    # print("Message", message)
                message_json = json.dumps(message).encode("utf-8")
                await producer.send_and_wait("order_notification", message_json)


    finally:
        await producer.stop()
        await consumer.stop()
        



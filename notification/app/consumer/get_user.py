from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.setting import BOOTSTRAP_SERVER
import json

async def get_user(notification_detail):
    print("Getting user..")
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    await producer.start()
    try:
        # print("Notification detail:", notification_detail)
        # notification_detail = json.loads(notification_detail
        
        notification_detail = json.dumps(notification_detail).encode("utf-8")
        await producer.send_and_wait("get_user",notification_detail)
    finally:    
        await producer.stop()
    
    


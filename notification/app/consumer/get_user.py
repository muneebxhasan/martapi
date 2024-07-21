from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.setting import BOOTSTRAP_SERVER
import json

async def get_user(user_id):
    print("Getting user..")
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    await producer.start()
    try:
        user ={
            "user_id": user_id
        }
        user_id = json.dumps(user).encode("utf-8")
        await producer.send_and_wait("get_user",user_id)
    finally:    
        await producer.stop()
    
    


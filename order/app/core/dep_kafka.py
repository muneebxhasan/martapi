from aiokafka import AIOKafkaProducer
from fastapi import Depends
from typing import Annotated


async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

Producer = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]


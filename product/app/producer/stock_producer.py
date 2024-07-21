from app.core.dp_kafka import Producer
import json

async def stock_producer(stock,producer:Producer):
    stock = json.dumps(stock).encode("utf-8")
    await producer.send_and_wait("add_stock",stock)
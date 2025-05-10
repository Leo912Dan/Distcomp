from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import asyncio
from typing import Dict, Any
from app.config.kafka import KAFKA_CONFIG, TOPICS
from app.models.message import Message

class KafkaService:
    def __init__(self):
        self.producer = None
        self.consumer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()

        self.consumer = AIOKafkaConsumer(
            TOPICS["OUT_TOPIC"],
            bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"],
            group_id=KAFKA_CONFIG["group_id"],
            auto_offset_reset=KAFKA_CONFIG["auto_offset_reset"],
            enable_auto_commit=KAFKA_CONFIG["enable_auto_commit"],
            auto_commit_interval_ms=KAFKA_CONFIG["auto_commit_interval_ms"]
        )
        await self.consumer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()

    async def send_message(self, message: Message):
        if not self.producer:
            raise RuntimeError("Kafka producer not initialized")
        
        # Используем topic_id как ключ для партиционирования
        await self.producer.send_and_wait(
            TOPICS["IN_TOPIC"],
            value=message.dict(),
            key=str(message.topic_id).encode('utf-8')
        )

    async def consume_messages(self, callback):
        if not self.consumer:
            raise RuntimeError("Kafka consumer not initialized")
        
        async for msg in self.consumer:
            try:
                message_data = json.loads(msg.value.decode('utf-8'))
                await callback(message_data)
            except Exception as e:
                print(f"Error processing message: {e}")

kafka_service = KafkaService() 
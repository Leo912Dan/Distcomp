from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_CONFIG: Dict[str, Any] = {
    "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    "group_id": os.getenv("KAFKA_GROUP_ID", "publisher-group"),
    "auto_offset_reset": "earliest",
    "enable_auto_commit": True,
    "auto_commit_interval_ms": 5000,
}

TOPICS = {
    "IN_TOPIC": "InTopic",
    "OUT_TOPIC": "OutTopic"
}

MESSAGE_STATES = {
    "PENDING": "PENDING",
    "APPROVE": "APPROVE",
    "DECLINE": "DECLINE"
} 
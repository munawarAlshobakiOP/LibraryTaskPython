import os
import json
from typing import Optional
from kafka import KafkaProducer
from kafka.errors import KafkaError
from app.schemas.internal_event import KafkaPublishFailed, InternalEvent

_producer: Optional[KafkaProducer] = None


def get_kafka_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        try:
            _producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                api_version_auto_timeout_ms=1000,
                request_timeout_ms=1000,
                max_block_ms=1000,
            )
        except Exception:
            return None
    return _producer


def publish_message(topic: str, message: dict):
    """
    Publishes a message to Kafka.
    """
    producer = get_kafka_producer()

    if producer is None:
        return KafkaPublishFailed(
            reason="Kafka producer is not initialized",
            topic=topic,
            original_error="Producer is None",
        )

    try:
        future = producer.send(topic, message)
        future.get(timeout=5)
        return None
    except Exception as e:
        return KafkaPublishFailed(
            reason="Failed to publish message to Kafka",
            topic=topic,
            original_error=str(e),
        )

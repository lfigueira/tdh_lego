"""Example Kafka consumer."""

import json
import os

from kafka import KafkaConsumer, KafkaProducer

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')

PUBLISH_TOPIC = os.environ.get('PUBLISH_TOPIC')

# waits 2 sec before producing
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
# TODO: needs to be tested
PRODUCER_LINGER_MS=2000


if __name__ == '__main__':
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )

    # TODO: investigate if needed to tune max_request_size
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
        linger_ms=PRODUCER_LINGER_MS
    )

    for message in consumer:
        # 
        transaction: dict = message.value

        transaction["mais"] = "BENFICA"

        # topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC

        producer.send(PUBLISH_TOPIC, value=transaction)

        print("Enriched transaction {}", transaction)  # DEBUG

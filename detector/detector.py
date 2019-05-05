"""Example Kafka consumer."""

import json
import os

from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')

PUBLISH_TOPIC = os.environ.get('PUBLISH_TOPIC')

# waits 2 sec before producing
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
# TODO: needs to be tested
PRODUCER_LINGER_MS=2000

def detect_accel_x(transaction):
    
    # break events
    # only uses accel_x
    # None if accel is zero; if positive assumes it's accelerating        
    if float(transaction["accel_x"]) < 0: 
        transaction["break_event"] = True
    elif float(transaction["accel_x"]) == 0: 
        transaction["break_event"] = None
    else: 
        transaction["break_event"] = False
    
    return transaction


def detect_rgt_curve(transaction):
    # turn left/right events
    # if yaw is positive assume it's a right turn, of left otherwise
    if float(transaction["gyro_yaw"]) > 0: 
        transaction["rgt_turn"] = True
    elif float(transaction["gyro_yaw"]) == 0: 
        transaction["rgt_turn"] = None
    else: 
        transaction["rgt_turn"] = False
    
    return transaction


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

    # create a mongoDB client
    client = MongoClient('mongosrv:27017')
    # create a collection
    collection = client.lego.test

    for message in consumer:        
        transaction: dict = message.value

        # enrich the transction
        # detect right/left curves
        transaction = detect_rgt_curve(transaction)
        
        # detect acceleration
        transaction = detect_accel_x(transaction)

        collection.insert_one(transaction)
        print('Message {} inserted into {}'.format(message, collection))

        # Can publish the enriched message to a new topic as well
        # producer.send(PUBLISH_TOPIC, value=transaction)
        # print("Enriched transaction {}", transaction)  # DEBUG

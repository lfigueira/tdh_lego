"""Loads data files into a Kafka topic."""

import os
from time import sleep
import json

import csv

from kafka import KafkaProducer

TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND


def run():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )

    ifname = "data/aggressive_longitudinal_acceleration_1549653321089461.csv"

    with open(ifname, 'r') as ifile:

        reader = csv.DictReader(ifile)

        for row in reader:
            transaction: dict = row

            producer.send(TRANSACTIONS_TOPIC, value=transaction)
            print(transaction)  # DEBUG
            sleep(SLEEP_TIME)


if __name__ == '__main__':
    run()
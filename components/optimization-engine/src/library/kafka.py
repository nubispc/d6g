# ProcessingSystems/kafka.py

from kafka import KafkaConsumer, KafkaProducer
from .config import kafka_bootstrap_servers, input_topic, output_topic

def consume_messages():
    from .messaging import process_message, logger  # Moved imports here

    consumer = KafkaConsumer(input_topic, bootstrap_servers=kafka_bootstrap_servers)
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

    for message in consumer:
        modified_message = process_message(message)
        if modified_message:
            producer.send(output_topic, modified_message.encode())

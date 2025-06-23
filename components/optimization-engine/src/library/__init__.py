# ProcessingSystems/__init__.py

# Import necessary modules and classes
from .rabbitmq import consume_messages as consume_rabbitmq_messages
from .kafka import consume_messages as consume_kafka_messages

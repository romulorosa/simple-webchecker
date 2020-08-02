import json
import logging

import backoff
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from components.consts import KAFKA_BROKER_CONNECT_MAX_TIME_SECONDS
from components.utils import (
    backoff_handler,
    giveup_backoff_handler,
    success_backoff_handler,
)


class BasicKafkaProducer:

    @backoff.on_exception(
        backoff.expo,
        NoBrokersAvailable,
        max_time=KAFKA_BROKER_CONNECT_MAX_TIME_SECONDS,
        on_backoff=backoff_handler,
        on_success=success_backoff_handler,
        on_giveup=giveup_backoff_handler,
    )
    def __init__(
            self,
            topic: str,
            bootstrap_servers: list,
            security_protocol: str = 'SSL',
            ssl_certfile: str = None,
            ssl_cafile: str = None,
            ssl_keyfile: str = None,
    ):

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10, 0),
            security_protocol=security_protocol,
            ssl_certfile=ssl_certfile,
            ssl_cafile=ssl_cafile,
            ssl_keyfile=ssl_keyfile,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        self.topic = topic

    def send_event(self, value: dict):
        try:
            return self.producer.send(self.topic, value)
        except TypeError:
            logging.error('Could not serialize object')

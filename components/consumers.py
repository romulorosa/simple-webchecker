import json
import logging
import backoff
from json import JSONDecodeError

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from components.consts import KAFKA_BROKER_CONNECT_MAX_TIME_SECONDS
from components.utils import (
    backoff_handler,
    success_backoff_handler,
    giveup_backoff_handler,
)


class BasicKafkaConsumer:

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
            group_id: str = None,
    ):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10, 0),
            security_protocol=security_protocol,
            ssl_certfile=ssl_certfile,
            ssl_cafile=ssl_cafile,
            ssl_keyfile=ssl_keyfile,
            group_id=group_id,
        )

    def start_consuming(self):
        """
        Starts consuming messages from Kafka Broker and validate their content
        """
        logging.info('Starting e-mail consumer')
        for msg in self.consumer:
            logging.debug('Message has arrived')
            try:
                yield json.loads(msg.value)
            except JSONDecodeError:
                logging.warning('Message with invalid JSON format. Discarding...')
                logging.debug(msg.value)

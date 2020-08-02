from components.consumers import BasicKafkaConsumer
from components.producers import BasicKafkaProducer
from components.migrations.database_schema import forwards
from components.monitors import BasicMonitor, MonitorScheduler
from components.processors import CheckerEventProcessor
from webchecker.settings import KAFKA


class CheckerCommandHandler:

    @classmethod
    def run(cls, regex, sites, interval):
        monitors = [BasicMonitor(site, regex) for site in sites]
        scheduler = MonitorScheduler(monitors, interval)
        producer = BasicKafkaProducer(
            KAFKA.topic,
            KAFKA.bootstrap_servers,
            ssl_certfile=KAFKA.ssl_certfile,
            ssl_cafile=KAFKA.ssl_cafile,
            ssl_keyfile=KAFKA.ssl_keyfile,
        )
        print('Producer has started')
        for value in scheduler.start():
            print(value)
            producer.send_event(value)


class WriterCommandHandler:

    @classmethod
    def run(cls):
        consumer = BasicKafkaConsumer(
            KAFKA.topic,
            KAFKA.bootstrap_servers,
            ssl_certfile=KAFKA.ssl_certfile,
            ssl_cafile=KAFKA.ssl_cafile,
            ssl_keyfile=KAFKA.ssl_keyfile,
        ).start_consuming()
        print('Consumer has started')

        for msg in consumer:
            print(msg)
            processor = CheckerEventProcessor()
            processor.save(msg)


class DatabaseSetupCommandHandler:

    @classmethod
    def run(cls):
        forwards()

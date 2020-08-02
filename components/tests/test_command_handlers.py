import mock
import pytest

from components.command_handlers import CheckerCommandHandler, WriterCommandHandler


@pytest.fixture
def mock_database_connection():
    with mock.patch('components.processors._database_connect') as m:
        m.return_value = mock.Mock(), mock.Mock()
        yield m


@pytest.fixture
def mock_kafka_consumer_next():
    with mock.patch('kafka.consumer.group.KafkaConsumer.__next__') as m:
        m.return_value = {}


@pytest.fixture
def mock_basic_kafka_consumer_start_consuming():
    with mock.patch('components.consumers.BasicKafkaConsumer.start_consuming') as m:
        m.return_value = [{}]
        yield m


@pytest.fixture
def mock_checker_event_processor_save():
    with mock.patch('components.processors.CheckerEventProcessor.save') as m:
        yield m


@pytest.fixture
def mock_basic_kafka_producer_send_event():
    with mock.patch('components.command_handlers.BasicKafkaProducer.send_event') as m:
        m.return_value = mock.Mock()
        yield m


@pytest.fixture
def scheduler_return_value(value=None):
    if not value:
        value = {}

    return value


@pytest.fixture
def mock_scheduler_start(scheduler_return_value):
    with mock.patch('components.monitors.MonitorScheduler.start') as m:
        m.return_value = [scheduler_return_value]
        yield m


def test_checker_command_handler_will_send_event(
    mock_kafka_producer,
    mock_scheduler_start,
    scheduler_return_value,
    mock_basic_kafka_producer_send_event,
):
    # given / when
    CheckerCommandHandler.run('.*', 'http://potato.com', 1)

    # then
    mock_basic_kafka_producer_send_event.assert_called_once_with(scheduler_return_value)


def test_writer_command_handler_will_save_event_to_database(
    mock_checker_event_processor_save,
    mock_kafka_consumer,
    mock_basic_kafka_consumer_start_consuming,
    mock_database_connection,
):
    # given / when
    handler = WriterCommandHandler.run()

    # then
    mock_checker_event_processor_save.assert_called_once()

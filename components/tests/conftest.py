import pytest
import mock


@pytest.fixture
def mock_kafka_producer():
    with mock.patch('kafka.KafkaProducer.__new__') as m:
        m.return_value = mock.Mock()
        yield m


@pytest.fixture
def mock_kafka_consumer():
    with mock.patch('kafka.KafkaConsumer.__new__') as m:
        m.return_value = mock.Mock()
        yield m
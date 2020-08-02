import mock
import pytest

from components.producers import BasicKafkaProducer


# @pytest.fixture
# def mock_kafka_producer():
#     with mock.patch('kafka.KafkaProducer.__new__') as m:
#         m.return_value = mock.Mock()
#         yield m


def test_producer_will_call_producer_send_on_send_event(mock_kafka_producer):
    # given
    topic = 'my_topic'
    value = {'test': 123}
    basic_producer = BasicKafkaProducer(topic, ['server:9092'])

    # when
    basic_producer.send_event(value)

    # then
    basic_producer.producer.send.assert_called_with(topic, value)

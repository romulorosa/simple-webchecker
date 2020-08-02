import mock
import pytest
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from components.monitors import BasicMonitor, MonitorScheduler


@pytest.fixture
def mock_monitor():
    return mock.Mock()


@pytest.fixture
def status_code(status_code=200):
    return status_code


@pytest.fixture
def response_time(time=1):
    return time


@pytest.fixture
def url(addr='http:://foo.bar'):
    return addr


@pytest.fixture
def content(data=''):
    return data


@pytest.fixture
def mock_basic_monitor_fetch(status_code, response_time, content):
    with mock.patch('components.monitors.BasicMonitor._fetch') as m:
        m.return_value = mock.Mock(
            status_code=status_code,
            elapsed=mock.Mock(total_seconds=lambda: response_time),
            content=content,
        )
        yield m


@pytest.mark.parametrize('status_code, response_time, url, matched', [
    (404, 0.4, 'https://notfound.com', False),
    (200, 1, 'http://foo.bar', True),
    (200, 2, 'http://potato.gemuse', True)
])
def test_basic_monitor_retrieve_data(
        mock_basic_monitor_fetch, status_code, response_time, url, matched
):
    # given
    basic_monitor = BasicMonitor(url)

    # when
    response = basic_monitor.retrieve_data()

    # then
    assert response['status_code'] == status_code
    assert response['response_time_seconds'] == response_time
    assert response['url'] == url
    assert response['match_pattern'] == matched


def test_monitor_will_call_retrieve_data_on_start(mock_monitor):
    # given
    scheduler = MonitorScheduler([mock_monitor], 1)

    # when
    next(scheduler.start())

    # then
    mock_monitor.retrieve_data.assert_called_once()


@pytest.fixture
def exception():
    return Timeout


@pytest.fixture
def mock_monitor_fetch_raises_exception(exception):
    with mock.patch('components.monitors.BasicMonitor._fetch') as m:
        m.side_effect = exception()
        yield m


@pytest.mark.parametrize('exception', [Timeout, ConnectionError])
def test_monitor_will_return_empty_dict_in_case_of_failure_fetching_data(
    mock_monitor_fetch_raises_exception, exception
):
    # given
    monitor = BasicMonitor('http://test.com')

    # when
    result = monitor.retrieve_data()

    # then
    assert result == {}

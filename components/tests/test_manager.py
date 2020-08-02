import pytest
import mock

from manage import (
    CheckerCommandHandler,
    WriterCommandHandler,
    DatabaseSetupCommandHandler,
)
from manage import exec_command
from components.consts import CLI_OPTS


@pytest.fixture
def command(cmd='checker'):
    return cmd


@pytest.fixture
def results(command):
    if command == CLI_OPTS['CHECKER']:
        return mock.Mock(command=command, regex='*.', sites='https://test.com', interval=1)
    return mock.Mock(command=command)


@pytest.fixture
def mock_handler_run(expected_handler):
    with mock.patch('components.command_handlers.{}.run'.format(expected_handler.__name__)) as m:
        m.return_value = None
        yield m


@pytest.mark.parametrize('command, expected_handler', [
    ('checker', CheckerCommandHandler),
    ('writer', WriterCommandHandler),
    ('setupdb', DatabaseSetupCommandHandler),
])
def test_exec_command_will_pick_the_correct_option(
    command, expected_handler, mock_handler_run, results,
):

    # given / when
    exec_command(results)

    # then
    mock_handler_run.assert_called_once()

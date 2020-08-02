import argparse
import validators

from components.command_handlers import (
    CheckerCommandHandler,
    WriterCommandHandler,
    DatabaseSetupCommandHandler,
)
from components.consts import CLI_OPTS


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='Webchecker commands', dest="command")


def url_validator(arg_value):
    if validators.url(arg_value):
        return arg_value
    raise argparse.ArgumentTypeError('You must specify valid URLs')


def exec_command(results):
    if results.command == CLI_OPTS['CHECKER']:
        CheckerCommandHandler.run(results.regex, results.sites, results.interval)
    elif results.command == CLI_OPTS['WRITER']:
        WriterCommandHandler.run()
    elif results.command == CLI_OPTS['SETUP_DB']:
        DatabaseSetupCommandHandler.run()


# Checker command
checker_parser = subparsers.add_parser(
    CLI_OPTS['CHECKER'],
    help='Starts a web checker'
)

checker_parser.add_argument(
    '-s',
    action='append',
    dest='sites',
    default=[],
    help='Websites address to be monitored',
    type=url_validator,
)

checker_parser.add_argument(
    '-i',
    action='store',
    dest='interval',
    default=60,
    type=int,
    help='Interval which the websites should be checked',
)

checker_parser.add_argument(
    '-r',
    action='store',
    dest='regex',
    default='.*',
    type=str,
    help='Regex pattern to be matched against the website content',
)

writer_parser = subparsers.add_parser(
    CLI_OPTS['WRITER'],
    help='Starts a database writer',
)

setupdb_parser = subparsers.add_parser(
    CLI_OPTS['SETUP_DB'],
    help='Sets up the database',
)


parser.add_argument('--version', action='version', version='%(prog)s 1.0')


input_result = parser.parse_args()
exec_command(input_result)


import logging

import psycopg2


def _database_connect(*args, **kwargs):
    conn = psycopg2.connect(*args, **kwargs)
    conn.autocommit = True

    cursor = conn.cursor()

    return conn, cursor


def backoff_handler(details: dict):
    logging.info(
        "Backing off {wait:0.1f} seconds after {tries} tries calling "
        "function {target} with args {args} and kwargs {kwargs}".format(**details)
    )


def success_backoff_handler(details: dict):
    logging.info("SUCCEEDED after {tries} tries and {elapsed} seconds".format(**details))


def giveup_backoff_handler(details: dict):
    logging.error("GAVE UP after {tries} tries and {elapsed} seconds".format(**details))
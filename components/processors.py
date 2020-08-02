import logging
from datetime import datetime

from components.utils import _database_connect
from webchecker import settings


class CheckerEventProcessor:

    def __init__(self):
        self.conn, self.cursor = _database_connect(
            database=settings.DATABASE.database,
            user=settings.DATABASE.username,
            password=settings.DATABASE.password,
            host=settings.DATABASE.hostname,
            port=settings.DATABASE.port,
        )

    def save(self, message):
        sql = """
            INSERT INTO webchecker_checks(ts, response_time_seconds, match_pattern, status_code, url)
            VALUES (%s, %s, %s, %s, '%s')
        """ % (
            datetime.timestamp(datetime.now()),
            message['response_time_seconds'],
            message['match_pattern'],
            message['status_code'],
            message['url'],
        )

        self.cursor.execute(sql)
        self.conn.close()
        logging.debug('Event saved')

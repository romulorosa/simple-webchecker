import logging
import sys

import requests
import re
from time import sleep
from typing import List
from http import HTTPStatus


class BasicMonitor:

    def __init__(self, url, regex='.*'):
        self.url = url
        self.regex = re.compile(regex)

    def _fetch(self):
        # TODO: This can be more efficient using asyncio
        response = requests.get(self.url, timeout=2)
        logging.debug('Content fetched')
        return response

    def retrieve_data(self):
        try:
            response = self._fetch()
        except requests.exceptions.Timeout:
            logging.error('Timeout fetching %s' % self.url)
            return {}
        except requests.exceptions.ConnectionError:
            logging.error('Network error connecting to %s' % self.url)
            return {}

        content = str(response.content)

        match_pattern = bool(self.regex.search(content)) \
            if response.status_code == HTTPStatus.OK else False

        return {
            'status_code': response.status_code,
            'response_time_seconds': response.elapsed.total_seconds(),
            'match_pattern': match_pattern,
            'url': self.url,
        }


class MonitorScheduler:

    def __init__(self, monitors: List[BasicMonitor], interval_seconds: int = 60):
        self.monitors = monitors
        self.interval = interval_seconds

    def start(self):
        try:
            while True:
                for monitor in self.monitors:
                    yield monitor.retrieve_data()
                sleep(self.interval)
        except KeyboardInterrupt:
            logging.info('Shutting down scheduler...')
            sys.exit(0)

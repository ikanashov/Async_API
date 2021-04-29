import logging
import os
import sys

import backoff

import requests
from requests.exceptions import ConnectionError

# this need to add script start dir to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from core.config import cnf

logging.getLogger('backoff').addHandler(logging.StreamHandler())


class IsNginxReady:

    @backoff.on_predicate(backoff.fibo, max_value=10)
    @backoff.on_exception(backoff.expo, ConnectionError)
    def ping(self) -> bool:
        if requests.get(cnf.NGINX_URL + '/api/openapi').status_code == 200:
            return True
        return False


IsNginxReady().ping()

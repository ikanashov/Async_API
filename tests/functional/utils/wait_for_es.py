import logging
import os
import sys

import backoff

from elasticsearch import Elasticsearch
from elasticsearch import ConnectionError as ESConnectionError

# this need to add script start dir to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from core.config import cnf

logging.getLogger('backoff').addHandler(logging.StreamHandler())

class IsESReady:
    def __init__(self):
        self.hosts = cnf.ELASTIC_HOST
        self.port = cnf.ELASTIC_PORT
        self.scheme = cnf.ELASTIC_SCHEME
        self.http_auth = (cnf.ELASTIC_USER, cnf.ELASTIC_PASSWORD)

        self.es = Elasticsearch(self.hosts, port=self.port, scheme=self.scheme, http_auth=self.http_auth)

    @backoff.on_predicate(backoff.fibo, max_value=10)
    @backoff.on_exception(backoff.expo, ESConnectionError)
    def ping(self) -> bool:
        if self.es.cluster.health(wait_for_status='green')['status'] == 'green':
            return True
        return False


IsESReady().ping()

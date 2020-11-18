import os

class Config(object):
    SECRET_KEY = os.urandom(32)
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 3600
    SPARQL_ENDPOINT = "https://bbip.askomics.org/virtuoso/sparql"
#    SPARQL_ENDPOINT = "http://0.0.0.0:80/virtuoso/sparql"
    PROXY_PREFIX="/test"

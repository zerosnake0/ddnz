import os
import requests

from ...conf import REQUESTS_TIMEOUT
from ...logger import logger


def update():
    logger.info("Updating Duck DNS")
    domains = os.environ["DDNZ_DUCKDNS_DOMAIN"]
    token = os.environ["DDNZ_DUCKDNS_TOEKN"]
    url = "https://www.duckdns.org/update?domains={}&token={}&verbose=true".format(domains, token)
    logger.debug("URL: %s", url)
    req = requests.get(url, timeout=REQUESTS_TIMEOUT)
    logger.debug("status_code: %s", req.status_code)
    logger.debug("content: %s", req.text)
    if req.ok and req.text.startswith('OK'):
        logger.info("Duck Dns has been updated successfully")
    else:
        logger.error("Error while updating DuckDns: %s, %s", req.ok, req.text)

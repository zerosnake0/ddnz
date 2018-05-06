import requests

from ...conf import REQUESTS_TIMEOUT
from ...logger import logger


def getip():
    url = "https://api.ipify.org/"
    logger.debug('Getting ip from %s', url)
    r = requests.get(url, timeout=REQUESTS_TIMEOUT)
    logger.debug('status_code: %s', r.status_code)
    logger.debug('content: %s', r.text)
    if r.ok:
        return r.text

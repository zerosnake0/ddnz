import os
import requests

from ddnz.logger import logger


def update():
    logger.info("Updating Duck DNS")
    domains = os.environ["DDNZ_DUCKDNS_DOMAIN"]
    token = os.environ["DDNZ_DUCKDNS_TOEKN"]
    url = "https://www.duckdns.org/update?domains={}&token={}&verbose=true".format(domains, token)
    logger.info("URL:%s", url)
    req = requests.get(url)
    if not (req.ok and req.text.startswith('OK')):
        logger.error("Error while updating DuckDns: %s %s", req.ok, req.text)
    else:
        logger.info("Duck Dns has been updated successfully")

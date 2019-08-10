import os
import uuid
import http
import http.server
import threading
import requests
from importlib import import_module

from ..conf import IP_CHECK_TIMEOUT
from ..logger import logger


def checkipformat(ip):
    try:
        lst = list(map(int, ip.split('.')))
        return len(lst) == 4 and all(0 <= i <= 255 for i in lst)
    except Exception as e:
        logger.debug("Error while checking ip format for %s: %s", ip, e)
        return False


def new_handler(msg):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(http.HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(msg.encode())

    return Handler


def checkip(ip, external_port, internal_port, proxy=""):
    # format check
    logger.info("Checking %s format", ip)
    if not checkipformat(ip):
        logger.error("Invalid ip format: %s", ip)
        return False

    # connection check
    logger.info("Checking %s with %s, %s", ip, external_port, internal_port)
    msg = uuid.uuid4().hex
    httpd = http.server.HTTPServer(('', internal_port), new_handler(msg))

    th = threading.Thread(target=httpd.serve_forever)
    th.start()

    url = "http://%s:%s" % (ip, external_port)

    try:
        try:
            resp = requests.get(url, timeout=IP_CHECK_TIMEOUT)
        except Exception as e:
            logger.error("unable to get without proxy: %s", e)
            if proxy == "":
                raise
            logger.info("trying with proxy...")
            resp = requests.get(url, timeout=IP_CHECK_TIMEOUT, proxies={"http": "http://" + proxy})
        resp.raise_for_status()
        logger.info("got message %s", resp.text)
        if resp.text != msg:
            return False
        logger.info("Matched")
        return True
    finally:
        logger.info("shutting down server")
        httpd.shutdown()
        logger.info("joining thread")
        th.join()
        logger.info("cleaned up")


def getip(external_port, internal_port, proxy=""):
    d = {}
    folder = os.path.join(os.path.dirname(__file__), 'sites')
    ip_success = set()
    for fname in os.listdir(folder):
        if not fname.endswith('.py'):
            continue

        if fname == '__init__.py':
            continue

        mname = fname[:-3]
        logger.info("Getting ip from %s", mname)
        try:
            m = import_module('.{}'.format(mname), 'ddnz.getip.sites')
            ip = m.getip()
            logger.info("Result from %s: %s", mname, ip)
            if ip in ip_success:
                logger.info("%s already verified", ip)
            elif checkip(ip, external_port, internal_port, proxy):
                logger.info("%s check success", ip)
                d[mname] = ip
                ip_success.add(ip)
            else:
                logger.info("%s check failed", ip)
        except Exception as e:
            logger.error("Unable to get ip from %s: %s", mname, e)
    return d

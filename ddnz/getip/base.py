import os
import socket
import uuid
from importlib import import_module

from ..conf import IP_CHECK_TIMEOUT
from ..logger import logger


def checkipformat(ip):
    try:
        l = map(int, ip.split('.'))
        return len(l) == 4 and all(i >= 0 and i <= 255 for i in l)
    except Exception as e:
        logger.debug("Error while checking ip format for %s: %s", ip, e)
        return False


def checkip(ip, external_port, internal_port):
    # format check
    logger.info("Checking %s format", ip)
    if not checkipformat(ip):
        logger.error("Invalid ip format: %s", ip)
        return False

    # connection check
    logger.info("Checking %s with %s, %s", ip, external_port, internal_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', internal_port))
    s.listen(1)
    logger.info("Listening at %s", s.getsockname())

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((ip, external_port))
    logger.info("Connected from %s to %s", c.getsockname(), c.getpeername())

    s.settimeout(IP_CHECK_TIMEOUT)
    conn, addr = s.accept()
    logger.info('Accepted at %s from %s', conn.getsockname(), conn.getpeername())

    msg = uuid.uuid4().hex
    c.sendall(msg)
    logger.info("Sent: %s", msg)
    conn.settimeout(IP_CHECK_TIMEOUT)

    recv_msg = ''
    length_left = len(msg)
    try:
        while length_left > 0:
            m = conn.recv(length_left)
            recv_msg += m
            logger.debug("Received: %s", recv_msg)
            if not msg.startswith(recv_msg):
                logger.info("Not matching")
                return False
            length_left -= len(m)
    finally:
        logger.info("Received: %s", recv_msg)

    if msg != recv_msg:
        return False

    logger.info("Matched")
    return True


def getip(external_port, internal_port):
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
            elif checkip(ip, external_port, internal_port):
                logger.info("%s check success", ip)
                d[mname] = ip
                ip_success.add(ip)
            else:
                logger.info("%s check failed", ip)
        except Exception as e:
            logger.exception("Unable to get ip from %s: %s", mname, e)
    return d

import os
import socket
import uuid
from importlib import import_module

from ddnz.logger import logger


def checkip(ip, external_port, internal_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', internal_port))
    s.listen(1)
    logger.info("Listening")
    
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((ip, external_port))
    logger.info("Connected")

    conn, addr = s.accept()
    logger.info('Accepted')
    msg = uuid.uuid4().bytes
    c.sendall(msg)
    if msg == conn.recv(len(msg)):
        logger.info("Matched")
        return True


def getip(external_port, internal_port):
    d = {}
    folder = os.path.join(os.path.dirname(__file__), 'sites')
    for fname in os.listdir(folder):
        if not fname.endswith('.py'):
            continue

        if fname == '__init__.py':
            continue

        mname = fname[:-3]
        try:
            m = import_module('.{}'.format(mname), 'ddnz.getip.sites')
            ip = m.getip()
            if checkip(ip, external_port, internal_port):
                d[mname] = ip
        except:
            logger.exception("Unable to get ip from {}".format(mname))
    return d

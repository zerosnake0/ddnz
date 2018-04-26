import os
import logging
import logging.config
import json
import time
from socket import gethostname
from getpass import getuser
import smtplib
from email.mime.text import MIMEText

import dns.resolver

from .conf import LOGGING, DATA_FILE
from .getip import getip
from .ddns import update
from .logger import logger


def getlastdata():
    logging.info("Loading data")
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
            assert isinstance(data, dict)
            return data
    except:
        logger.exception("Unable to get last data")
        return {}


def savedata(d):
    logging.info("Saving data")
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(d, f)
    except:
        logger.exception("Unable to save data")


def resolve(dst):
    logger.info("Resolving %s", dst)
    _, _, site = dst.partition('@')

    ans = dns.resolver.query(site, 'MX')
    ans = [(a.preference, a.exchange) for a in ans]
    ans.sort(reverse=True)
    for a in ans:
        logger.info(a)
    return ans[0][1].to_text().rstrip('.')


def report(dip):
    dst = os.getenv('DDNZ_MAIL_DST')
    if dst:
        logging.info("Reporting")
        try:
            mx = resolve(dst)
            content = "user: {}\n".format(getuser())
            content += "host: {}\n".format(gethostname())
            content += ''.join(['{}: {}\n'.format(k, v) for k, v in dip.items()])
            msg = MIMEText(content)
            msg['Subject'] = 'IP Report'
            msg['From'] = 'ddnz@ddnz.local'
            msg['To'] = dst
            s = smtplib.SMTP(mx)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            s.quit()
            return True
        except:
            logger.exception("Unable to report")


def main():
    logging.config.dictConfig(LOGGING)
    logging.info("Started")
    ext_port = int(os.environ['DDNZ_EXT_PORT'])
    int_port = int(os.environ['DDNZ_INT_PORT'])

    data = getlastdata()
    dip = getip(ext_port, int_port)

    old_ip = data.get('ip')
    new_ip = None
    for ip in dip.values():
        if ip != old_ip:
            new_ip = ip
            break

    updated = False
    if new_ip is None:
        logger.info("IP not changed")
    else:
        logger.info("IP changed from %s to %s", old_ip, new_ip)
        update()
        data['ip'] = new_ip
        updated = True

    old_ts = data.get('ts', 0)
    ts = time.time()
    delta = ts - old_ts
    logger.info("elapsed %.2f", delta)
    try:
        period = float(os.getenv('DDNZ_MAIL_PERIOD', '900'))
        logger.info("period %.2f", period)
        if delta > period and report(dip):
            data['ts'] = ts
            updated = True
    except:
        logger.exception("Error while checking reporting")

    if updated:
        savedata(data)

    logging.info("Ended")


if __name__ == '__main__':
    main()

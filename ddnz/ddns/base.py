import os
from importlib import import_module

from ..logger import logger


def update():
    folder = os.path.join(os.path.dirname(__file__), 'sites')
    for fname in os.listdir(folder):
        if not fname.endswith('.py'):
            continue

        if fname == '__init__.py':
            continue

        mname = fname[:-3]
        logger.info("Updating ip from %s", mname)
        try:
            m = import_module('.{}'.format(mname), 'ddnz.ddns.sites')
            m.update()
            logger.info("Update from %s success", mname)
        except Exception as e:
            logger.exception("Unable to update from %s: %s", mname, e)

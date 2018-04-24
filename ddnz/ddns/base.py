import os
from importlib import import_module

from ddnz.logger import logger


def update():
    folder = os.path.join(os.path.dirname(__file__), 'sites')
    for fname in os.listdir(folder):
        if not fname.endswith('.py'):
            continue

        if fname == '__init__.py':
            continue

        mname = fname[:-3]
        try:
            m = import_module('.{}'.format(mname), 'ddnz.ddns.sites')
            m.update()
        except:
            logger.exception("Unable to update from {}".format(mname))

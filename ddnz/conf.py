import os
from tempfile import gettempdir

tempdir = gettempdir()

DATA_FILE = os.path.join(tempdir, 'ddnz_ip.txt')
REQUESTS_TIMEOUT = int(os.getenv('DDNZ_REQUESTS_TIMEOUT', '10'))
IP_CHECK_TIMEOUT = int(os.getenv('DDNZ_IP_CHECK_TIMEOUT', '10'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname).1s %(asctime)s [%(module)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler'
        },
        'error': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(tempdir, 'ddnz_err.log'),
            'maxBytes': 20000,
            'encoding': 'utf8'
        },
        'info': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(tempdir, 'ddnz_info.log'),
            'maxBytes': 20000,
            'encoding': 'utf8'
        }
    },
    'root': {
        'handlers': ['console', 'error', 'info'],
        'level': 'DEBUG'
    }
}

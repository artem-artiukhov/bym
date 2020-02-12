import logging
from logging.config import dictConfig

from flask.logging import default_handler

from microblog.config import LOG_LEVEL

log = logging.getLogger()
log.addHandler(default_handler)


def setup_logging():
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s.%(msecs)03d] [%(levelname)s] '
                          '[%(module)s:%(lineno)s] [%(name)s] %(message)s',
                'datefmt': '%b/%d/%Y %H:%M:%S'
            }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }},
        'root': {
            'level': LOG_LEVEL,
            'handlers': ['wsgi']
        },
        'loggers': {
            'alembic': {
                'level': LOG_LEVEL,
                'handlers': ['wsgi']
            }}
    })

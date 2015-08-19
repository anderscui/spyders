import logging

logging.warning('This is a warning')
logging.info('This is a warning')

logging.log(logging.WARNING, 'info')

logger = logging.getLogger('mylogger')
logger.warning('my logger:)')

logger = logging.getLogger(__name__)
logging.warning('warning')
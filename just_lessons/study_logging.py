import logging
import sys

# logging.basicConfig(
#     level=logging.CRITICAL,
#     format='[{asctime}] #{levelname:8} {filename}:'
#             '{lineno} - {name} - {message}',
#     style='{'
# )

format='[{asctime}] #{levelname:8} {filename}:{lineno} - {name} - {message}'

formatter = logging.Formatter(
    fmt=format,
    style='{'
)

class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        # print(dir(record))
        return record.levelname == 'WARNING' and 'важно' in record.msg.lower()

logger = logging.getLogger(__name__)

stderr_handler = logging.StreamHandler()
# stdout_handler = logging.StreamHandler(sys.stdout)

stderr_handler.setFormatter(formatter)
stderr_handler.addFilter(ErrorLogFilter())

# logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)

# file_handler = logging.FileHandler('log.txt')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)




# logging.debug('Это лог уровня DEBUG')
# logging.info('Это лог уровня INFO')
logger.warning('This is the log which type is WARNING важно')
# logging.error('Это лог уровня ERROR')
# logging.critical('Это лог уровня CRITICAL')
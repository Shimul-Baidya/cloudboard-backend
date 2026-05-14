import logging
import sys

logger = logging.getLogger('apps')
logger.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')

stream_handler.setLevel(logging.INFO)

# set formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handlers to the logger
if not logger.handlers:
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
import logging
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename = "/home/taitz/Documents/Python/urlshortener/logs.log", level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()
# logger.info("Out first message.")
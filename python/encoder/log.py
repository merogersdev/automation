import logging
from sys import stdout


def setup_logger(name):
    log_format = "%(levelname)s | %(asctime)s | %(message)s"
    date_format = "%Y-%m-%d %I:%M %p"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    filehandler = logging.FileHandler("encoder.log")
    handler = logging.StreamHandler(stdout)
    formatter = logging.Formatter(log_format, date_format)
    handler.setFormatter(formatter)
    filehandler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(filehandler)

    setup_logger('Encoder')


logger = logging.getLogger('Encoder')

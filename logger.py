import logging
import sys

from config import LOG_LEVEL, LOG_FORMAT


def get_logger(name: str = "rubika_uploader") -> logging.Logger:
    """
    Create and return a configured logger.
    Prevents duplicate handlers when imported multiple times.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    formatter = logging.Formatter(LOG_FORMAT)

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger


logger = get_logger()
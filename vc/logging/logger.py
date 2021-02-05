import logging


class Logger:
    def __init__(self, logging_level=logging.INFO):
        logging.basicConfig(level=logging_level)

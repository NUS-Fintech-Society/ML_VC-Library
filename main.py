import logging
from mlvc.config import config
from mlvc.logging.logger import Logger


def main():
    Logger(config.LOGGING_LEVEL)
    logging.info("Logger successfully initialized, running main.py")


if __name__ == "__main__":
    main()

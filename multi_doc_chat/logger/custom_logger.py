import os
import sys
import logging
from datetime import datetime
from typing import Optional
import structlog

_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class CustomLogger:
    _instance: Optional["CustomLogger"] = None
    _configured: bool = False

    def __new__(cls, log_dir: str = "logs"):
        if cls._instance is None:
            cls._instance = super(CustomLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_dir: str = "logs"):
        if self._configured:
            return

        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)

        # Configure root logger for standard Python logging
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        if not root_logger.handlers:
            file_handler = logging.FileHandler(self.log_file_path, encoding="utf-8")
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

            root_logger.addHandler(file_handler)
            root_logger.addHandler(console_handler)

        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        self._default_logger = structlog.get_logger("CustomLogger")
        CustomLogger._configured = True

    def get_logger(self, name: str = __file__):
        if not name:
            logger_name = "default"
        elif isinstance(name, str):
            logger_name = os.path.basename(name) if ("/" in name or "\\" in name) else name
        else:
            logger_name = str(name)

        return structlog.get_logger(logger_name)

    def info(self, event: str, *args, **kwargs):
        return self._default_logger.info(event, *args, **kwargs)

    def warning(self, event: str, *args, **kwargs):
        return self._default_logger.warning(event, *args, **kwargs)

    def error(self, event: str, *args, **kwargs):
        return self._default_logger.error(event, *args, **kwargs)

    def debug(self, event: str, *args, **kwargs):
        return self._default_logger.debug(event, *args, **kwargs)

    def critical(self, event: str, *args, **kwargs):
        return self._default_logger.critical(event, *args, **kwargs)

    def exception(self, event: str, *args, **kwargs):
        return self._default_logger.exception(event, *args, **kwargs)


def get_logger(name: str = __file__):
    """Helper function to get a logger instance by name."""
    return CustomLogger().get_logger(name)


# Global singleton logger instance
GLOBAL_LOGGER = get_logger("GLOBAL")


def info(event: str, *args, **kwargs):
    return GLOBAL_LOGGER.info(event, *args, **kwargs)


def warning(event: str, *args, **kwargs):
    return GLOBAL_LOGGER.warning(event, *args, **kwargs)


def error(event: str, *args, **kwargs):
    return GLOBAL_LOGGER.error(event, *args, **kwargs)


def debug(event: str, *args, **kwargs):
    return GLOBAL_LOGGER.debug(event, *args, **kwargs)


def critical(event: str, *args, **kwargs):
    return GLOBAL_LOGGER.critical(event, *args, **kwargs)


def exception(event: str, *args, **kwargs):
    return GLOBAL_LOGGER.exception(event, *args, **kwargs)
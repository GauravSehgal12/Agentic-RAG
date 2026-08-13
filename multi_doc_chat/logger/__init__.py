from multi_doc_chat.logger.custom_logger import (
    CustomLogger,
    GLOBAL_LOGGER,
    get_logger,
    info,
    warning,
    error,
    debug,
    critical,
    exception,
)

logger = GLOBAL_LOGGER

__all__ = [
    "CustomLogger",
    "GLOBAL_LOGGER",
    "logger",
    "get_logger",
    "info",
    "warning",
    "error",
    "debug",
    "critical",
    "exception",
]

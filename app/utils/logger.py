"""Logging configuration"""

import logging
import sys
from app.config import get_settings

settings = get_settings()


def setup_logging():
    """Configure logging for the application"""
    log_level = getattr(logging, settings.LOG_LEVEL.upper())

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)

    return root_logger


# Initialize logger
logger = setup_logging()

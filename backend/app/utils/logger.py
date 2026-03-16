# Logging system, provides centralized logging with file and console output

import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

from ..config import config


# Sets up the application logger with file and console handlers
def setup_logger():
    # Create logger
    logger = logging.getLogger("shiina")
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    simple_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s - %(message)s", datefmt="%H:%M:%S"
    )

    # file handler (if enabled)
    if config.LOG_TO_FILE:
        # Ensure logs directory exists
        config.LOGS_DIR.mkdir(exist_ok=True)

        log_file = config.LOGS_DIR / f"shiina {datetime.now().strftime('%Y%m%d')}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    # Console handler (if enabled)
    if config.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)

    return logger


# Create and export logger instance
logger = setup_logger()

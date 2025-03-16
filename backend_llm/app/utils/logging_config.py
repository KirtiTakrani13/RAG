import logging
import json
from app.utils.settings import LOG_LEVEL, LOG_FILE  # ✅ Import only settings

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    """
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "filename": record.filename,
            "lineno": record.lineno,
            "funcName": record.funcName,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def get_logger():
    """
    Set up logging with both file and console handlers.
    """
    logger = logging.getLogger("app_logger")
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:  # Avoid adding duplicate handlers
        formatter = JSONFormatter()

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

import logging
import sys

# Configure standard formatting for logging
logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=logging_format,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance for the given module name.
    """
    return logging.getLogger(name)

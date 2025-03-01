import logging
from pathlib import Path

def setup_logging(enable_file_logging=False):
    """Sets up basic logging for the application, with optional file logging using pathlib."""
    # Create a logger
    logger = logging.getLogger('atoms')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    # Create console handler and set level to info
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)

    # Optionally add file handler if enabled
    if enable_file_logging:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'app.log'

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Setup logging with file logging disabled by default
logger = setup_logging(enable_file_logging=False)

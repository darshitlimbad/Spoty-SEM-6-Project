import logging
import colorlog

def setup_logger():
    # Create a StreamHandler with color formatting
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s %(asctime)s %(levelname)s: %(message)s"
    ))

    # Create and configure the logger
    logger = colorlog.getLogger('colored_logger')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

logger= setup_logger()
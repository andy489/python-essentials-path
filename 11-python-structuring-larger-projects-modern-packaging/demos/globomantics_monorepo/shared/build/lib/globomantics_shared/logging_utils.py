import logging
from logging import Logger

def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure basic logging format for the entire application.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )


def get_logger(name: str) -> Logger:
    """
    Return a module-level logger.
    """
    return logging.getLogger(name)

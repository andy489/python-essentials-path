import logging


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(name)s: %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

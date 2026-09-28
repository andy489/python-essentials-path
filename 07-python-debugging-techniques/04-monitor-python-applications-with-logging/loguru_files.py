import time

from loguru import logger

logger.add(
    "logs/info_{time:YYYY-MM-DD_HH-mm-ss}.log",
    rotation="5 seconds",
    retention="30 seconds",
    format="{message}",
    serialize=True,
)

for i in range(60):
    logger.info(f"This is log {i + 1}")
    time.sleep(1)

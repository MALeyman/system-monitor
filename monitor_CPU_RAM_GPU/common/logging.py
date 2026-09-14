"""Единая точка настройки логирования."""
import logging


def setup_logging(level: int = logging.INFO, filename: str = "monitor.log") -> None:
    logging.basicConfig(
        level=level,
        filename=filename,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
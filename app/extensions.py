import logging
from flask import Flask

def configure_logging(app: Flask, level: str) -> None:
    numeric_level = getattr(logging, level, logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(numeric_level)

    # Evita duplicar handlers
    if not root.handlers:
        root.addHandler(handler)

    app.logger.setLevel(numeric_level)

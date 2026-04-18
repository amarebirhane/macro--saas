import logging
import sys
from pathlib import Path


def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    from app.core.config import settings

    logHandler = logging.StreamHandler(sys.stdout)

    if settings.ENVIRONMENT == "production":
        from pythonjsonlogger import jsonlogger

        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s"
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    logHandler.setFormatter(formatter)

    fileHandler = logging.FileHandler(log_dir / "app.log")
    fileFormatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    )
    fileHandler.setFormatter(fileFormatter)

    # Configure logging
    logging.basicConfig(level=logging.INFO, handlers=[logHandler, fileHandler])

    # Set specific levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


logger = logging.getLogger("app")

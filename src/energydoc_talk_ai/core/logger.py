import sys
from pathlib import Path
from loguru import logger
from energydoc_talk_ai.core.config import settings


def setup_logger(
    logger_name: str | None = None,
    *,
    log_name: str = "energydoc_talk_ai.log",
    level: str = "INFO",
):
    """
    Configure le logger global.
    """
    # -----------------------------
    # Supprimer les handlers existants
    # -----------------------------
    logger.remove()

    # -----------------------------
    # Bind extra metadata correctly
    # -----------------------------
    bound_logger = logger.bind(logger_name=logger_name or "--")

    # -------------------------------
    # Handler console
    # -------------------------------
    bound_logger.add(
        sys.stdout,
        level=level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<magenta>{extra[logger_name]}</magenta> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    # -------------------------------
    # Handler fichier
    # -------------------------------
    bound_logger.add(
        f"{settings.logs_dir}/{log_name}",
        rotation="20 MB",
        retention="30 days",
        compression="zip",
        level=level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level} | "
            "{extra[logger_name]} | "
            "{name}:{function}:{line} - {message}"
        ),
    )

    #bound_logger.info(f"Loguru logger initialized. (logger_name='{logger_name}')")

    return bound_logger

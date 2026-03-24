import logging
from pathlib import Path


def setup_logging(cfg: dict) -> logging.Logger:
    """
    Configure application logging from config.json.
    """
    project_root = Path(__file__).resolve().parents[1]

    log_cfg = cfg.get("logging", {})
    log_file = log_cfg.get("file", "logs/airport_flights.log")
    level_name = log_cfg.get("level", "INFO")
    fmt = log_cfg.get(
        "format",
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    log_path = (project_root / log_file).resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("flight")
    logger.setLevel(getattr(logging, level_name.upper(), logging.INFO))
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter(fmt)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

from loguru import logger
from pathlib import Path

def set_logger():
    log_dir = Path.cwd() / "logs"
    log_dir.mkdir(exist_ok=True)

    logger.remove()

    logger.add(
        log_dir / "app.log",
        level="INFO",
        rotation="1 GB",
        retention="14 days",
        compression="gz",
        colorize=True,
        backtrace=True, 
        diagnose=True,
        format="<blue>{time:DD-MM-YYYY HH:mm:ss}</blue> | {level} | {message}",
    )

    logger.add(
        log_dir / "error.log",
        level="ERROR",
        rotation="100 MB",
        retention="1 month",
        compression="gz",
        colorize=True,
        backtrace=True,
        diagnose=True,
        format="<red>{time:DD-MM-YYYY HH:mm:ss}</red> | {level} | {name}:{line} | {message}"
    )   

    return logger
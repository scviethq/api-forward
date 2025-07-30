import sys
from pathlib import Path
from loguru import logger
from app.config import config


def setup_logger():
    """Setup loguru logger with rotation and configuration"""
    
    # Remove default logger
    logger.remove()
    
    # Create logs directory if not exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Add console logger
    logger.add(
        sys.stdout,
        format=config.logging.format,
        level=config.server.log_level,
        colorize=True
    )
    
    # Add file logger with rotation
    logger.add(
        logs_dir / "forward.log",
        format=config.logging.format,
        level=config.server.log_level,
        rotation=config.logging.rotation,
        retention=config.logging.retention,
        compression=config.logging.compression,
        backtrace=True,
        diagnose=True
    )
    
    # Add error log file
    logger.add(
        logs_dir / "error.log",
        format=config.logging.format,
        level="ERROR",
        rotation=config.logging.rotation,
        retention=config.logging.retention,
        compression=config.logging.compression,
        backtrace=True,
        diagnose=True
    )
    
    logger.info("Logger setup completed")


# Setup logger when module is imported
setup_logger() 
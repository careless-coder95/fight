"""
Custom Logger Configuration
Provides colorful console and file logging
"""

import logging
import colorlog
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory
Path("logs").mkdir(exist_ok=True)

# Color scheme
LOG_COLORS = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}

def setup_logger(name: str = "TelegramVCRelay", level: str = "INFO") -> logging.Logger:
    """
    Setup colorful logger with file and console handlers
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s%(asctime)s %(levelname)-8s%(reset)s %(blue)s[%(name)s]%(reset)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors=LOG_COLORS
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler for all logs
    file_handler = RotatingFileHandler(
        'logs/bot.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    file_formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Error file handler
    error_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger

def setup_stream_logger(name: str = "StreamEngine") -> logging.Logger:
    """Setup logger for stream engine"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Stream file handler
    stream_handler = RotatingFileHandler(
        'logs/stream.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )
    stream_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(stream_handler)
    
    return logger

def setup_ffmpeg_logger(name: str = "FFmpeg") -> logging.Logger:
    """Setup logger for FFmpeg operations"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # FFmpeg file handler
    ffmpeg_handler = RotatingFileHandler(
        'logs/ffmpeg.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=2
    )
    ffmpeg_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    ffmpeg_handler.setFormatter(formatter)
    
    logger.addHandler(ffmpeg_handler)
    
    return logger

# Create default loggers
main_logger = setup_logger()
stream_logger = setup_stream_logger()
ffmpeg_logger = setup_ffmpeg_logger()

"""
Helper Utilities
Common helper functions
"""

import time
import psutil
from typing import Optional
from pyrogram.types import Message
from config import config

def get_readable_time(seconds: int) -> str:
    """
    Convert seconds to readable time format
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def get_readable_size(size_bytes: int) -> str:
    """
    Convert bytes to readable size format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def get_system_stats() -> dict:
    """
    Get system statistics
    
    Returns:
        System stats dictionary
    """
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "cpu_percent": cpu_percent,
        "cpu_cores": psutil.cpu_count(),
        "memory_total": get_readable_size(memory.total),
        "memory_used": get_readable_size(memory.used),
        "memory_percent": memory.percent,
        "disk_total": get_readable_size(disk.total),
        "disk_used": get_readable_size(disk.used),
        "disk_percent": disk.percent,
    }

def get_bot_uptime(start_time: float) -> str:
    """
    Get bot uptime
    
    Args:
        start_time: Bot start timestamp
        
    Returns:
        Uptime string
    """
    
    uptime_seconds = int(time.time() - start_time)
    return get_readable_time(uptime_seconds)

def is_admin(user_id: int) -> bool:
    """
    Check if user is admin
    
    Args:
        user_id: User ID
        
    Returns:
        True if user is admin
    """
    
    return user_id in config.SUDO_USERS

async def check_admin(message: Message) -> bool:
    """
    Check if message sender is admin
    
    Args:
        message: Pyrogram message
        
    Returns:
        True if sender is admin
    """
    
    if not message.from_user:
        return False
    
    return is_admin(message.from_user.id)

async def is_group_admin(message: Message) -> bool:
    """
    Check if user is group admin
    
    Args:
        message: Pyrogram message
        
    Returns:
        True if user is group admin
    """
    
    if not message.from_user or not message.chat:
        return False
    
    try:
        member = await message.chat.get_member(message.from_user.id)
        return member.status in ["creator", "administrator"]
    except:
        return False

def format_volume_level(level: int) -> str:
    """
    Format volume level display
    
    Args:
        level: Volume level (1-25)
        
    Returns:
        Formatted string
    """
    
    bars = "█" * level + "░" * (25 - level)
    percentage = (level / 25) * 100
    return f"{bars} {level}/25 ({percentage:.0f}%)"

def format_bass_level(level: int) -> str:
    """
    Format bass reduction level display
    
    Args:
        level: Bass reduction level (0-15)
        
    Returns:
        Formatted string
    """
    
    bars = "█" * level + "░" * (15 - level)
    return f"{bars} {level}/15"

def get_progress_bar(current: int, total: int, length: int = 20) -> str:
    """
    Generate progress bar
    
    Args:
        current: Current value
        total: Total value
        length: Bar length
        
    Returns:
        Progress bar string
    """
    
    if total == 0:
        return "░" * length
    
    filled = int((current / total) * length)
    return "█" * filled + "░" * (length - filled)

def clean_filename(filename: str) -> str:
    """
    Clean filename for safe usage
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename
    """
    
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to max length
    
    Args:
        text: Original text
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."

async def delete_message_after(message: Message, seconds: int = 5):
    """
    Delete message after specified seconds
    
    Args:
        message: Pyrogram message
        seconds: Delay in seconds
    """
    
    import asyncio
    
    try:
        await asyncio.sleep(seconds)
        await message.delete()
    except:
        pass

def validate_volume_level(level: int) -> Optional[int]:
    """
    Validate and clamp volume level
    
    Args:
        level: Volume level
        
    Returns:
        Valid volume level or None
    """
    
    if level < 1 or level > config.MAX_VOLUME:
        return None
    
    return level

def validate_bass_level(level: int) -> Optional[int]:
    """
    Validate and clamp bass reduction level
    
    Args:
        level: Bass reduction level
        
    Returns:
        Valid bass level or None
    """
    
    if level < 0 or level > 15:
        return None
    
    return level

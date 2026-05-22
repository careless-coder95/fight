"""
Decorators
Useful decorators for command handlers
"""

import functools
from typing import Callable
from pyrogram.types import Message
from config import config, main_logger

def admin_only(func: Callable) -> Callable:
    """
    Decorator to restrict command to admins only
    
    Usage:
        @admin_only
        async def my_command(client, message):
            ...
    """
    
    @functools.wraps(func)
    async def wrapper(client, message: Message):
        if not message.from_user:
            return
        
        if message.from_user.id not in config.SUDO_USERS:
            await message.reply_text(
                "❌ **Permission Denied**\n\n"
                "This command is only available to bot administrators."
            )
            main_logger.warning(
                f"Unauthorized access attempt by {message.from_user.id} "
                f"to command: {func.__name__}"
            )
            return
        
        return await func(client, message)
    
    return wrapper

def group_only(func: Callable) -> Callable:
    """
    Decorator to restrict command to groups only
    
    Usage:
        @group_only
        async def my_command(client, message):
            ...
    """
    
    @functools.wraps(func)
    async def wrapper(client, message: Message):
        if message.chat.type not in ["group", "supergroup"]:
            await message.reply_text(
                "❌ **Invalid Chat Type**\n\n"
                "This command can only be used in groups."
            )
            return
        
        return await func(client, message)
    
    return wrapper

def require_voice_chat(func: Callable) -> Callable:
    """
    Decorator to check if voice chat is active
    
    Usage:
        @require_voice_chat
        async def my_command(client, message):
            ...
    """
    
    @functools.wraps(func)
    async def wrapper(client, message: Message):
        from core.vc_manager import vc_manager
        
        if not vc_manager.is_in_voice_chat(message.chat.id):
            await message.reply_text(
                "❌ **Not in Voice Chat**\n\n"
                "Assistant is not connected to voice chat.\n"
                "Use /join to connect first."
            )
            return
        
        return await func(client, message)
    
    return wrapper

def error_handler(func: Callable) -> Callable:
    """
    Decorator to handle errors gracefully
    
    Usage:
        @error_handler
        async def my_command(client, message):
            ...
    """
    
    @functools.wraps(func)
    async def wrapper(client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            main_logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            
            try:
                await message.reply_text(
                    "❌ **An Error Occurred**\n\n"
                    f"Error: `{str(e)}`\n\n"
                    "Please try again or contact support."
                )
            except:
                pass
    
    return wrapper

def typing_action(func: Callable) -> Callable:
    """
    Decorator to show typing action
    
    Usage:
        @typing_action
        async def my_command(client, message):
            ...
    """
    
    @functools.wraps(func)
    async def wrapper(client, message: Message):
        async with client.send_chat_action(message.chat.id, "typing"):
            return await func(client, message)
    
    return wrapper

def rate_limit(seconds: int = 5):
    """
    Decorator to rate limit command usage
    
    Usage:
        @rate_limit(seconds=10)
        async def my_command(client, message):
            ...
    """
    
    from time import time
    
    last_called = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(client, message: Message):
            user_id = message.from_user.id if message.from_user else 0
            
            now = time()
            if user_id in last_called:
                time_passed = now - last_called[user_id]
                if time_passed < seconds:
                    remaining = int(seconds - time_passed)
                    await message.reply_text(
                        f"⏳ **Rate Limited**\n\n"
                        f"Please wait {remaining} seconds before using this command again."
                    )
                    return
            
            last_called[user_id] = now
            return await func(client, message)
        
        return wrapper
    
    return decorator

def log_command(func: Callable) -> Callable:
    """
    Decorator to log command usage
    
    Usage:
        @log_command
        async def my_command(client, message):
            ...
    """
    
    @functools.wraps(func)
    async def wrapper(client, message: Message):
        user = message.from_user
        chat = message.chat
        
        user_info = f"{user.first_name} ({user.id})" if user else "Unknown"
        chat_info = f"{chat.title} ({chat.id})" if hasattr(chat, 'title') else str(chat.id)
        
        main_logger.info(
            f"Command: {func.__name__} | User: {user_info} | Chat: {chat_info}"
        )
        
        return await func(client, message)
    
    return wrapper

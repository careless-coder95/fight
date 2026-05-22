"""
Admin Module
Audio control commands for admins
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from core.stream_engine import stream_manager
from database import db
from utils.decorators import admin_only, group_only, require_voice_chat, error_handler, log_command
from utils.helpers import format_volume_level, format_bass_level, validate_volume_level, validate_bass_level
from config import config

@Client.on_message(filters.command("level") & filters.group)
@admin_only
@group_only
@require_voice_chat
@error_handler
@log_command
async def set_volume_level(client: Client, message: Message):
    """Handle /level command"""
    
    # Get level from command
    try:
        level = int(message.command[1]) if len(message.command) > 1 else None
    except (ValueError, IndexError):
        level = None
    
    # Validate level
    if level is None or validate_volume_level(level) is None:
        await message.reply_text(
            "❌ **Invalid Volume Level**\n\n"
            f"Please provide a level between 1 and {config.MAX_VOLUME}\n\n"
            f"Usage: `/level <1-{config.MAX_VOLUME}>`\n"
            f"Example: `/level 15`"
        )
        return
    
    chat_id = message.chat.id
    
    # Update in database
    settings = await db.get_settings(chat_id)
    settings["volume"] = level
    await db.save_settings(chat_id, settings)
    
    # Update stream if active
    stream = stream_manager.get_stream(chat_id)
    if stream:
        await stream.update_volume(level)
    
    await message.reply_text(
        f"✅ **Volume Level Updated**\n\n"
        f"🔊 {format_volume_level(level)}\n\n"
        f"⚠️ **Note:** Changes will take effect on next stream restart."
    )

@Client.on_message(filters.command("bass") & filters.group)
@admin_only
@group_only
@require_voice_chat
@error_handler
@log_command
async def set_bass_reduction(client: Client, message: Message):
    """Handle /bass command"""
    
    # Get level from command
    try:
        level = int(message.command[1]) if len(message.command) > 1 else None
    except (ValueError, IndexError):
        level = None
    
    # Validate level
    if level is None or validate_bass_level(level) is None:
        await message.reply_text(
            "❌ **Invalid Bass Reduction Level**\n\n"
            "Please provide a level between 0 and 15\n\n"
            "Usage: `/bass <0-15>`\n"
            "Example: `/bass 8`"
        )
        return
    
    chat_id = message.chat.id
    
    # Update in database
    settings = await db.get_settings(chat_id)
    settings["bass_reduction"] = level
    await db.save_settings(chat_id, settings)
    
    # Update stream if active
    stream = stream_manager.get_stream(chat_id)
    if stream:
        await stream.update_bass_reduction(level)
    
    await message.reply_text(
        f"✅ **Bass Reduction Updated**\n\n"
        f"🎵 {format_bass_level(level)}\n\n"
        f"ℹ️ Higher values = more bass reduction = clearer voice\n\n"
        f"⚠️ **Note:** Changes will take effect on next stream restart."
    )

@Client.on_message(filters.command("mute") & filters.group)
@admin_only
@group_only
@require_voice_chat
@error_handler
@log_command
async def mute_playback(client: Client, message: Message):
    """Handle /mute command"""
    
    chat_id = message.chat.id
    
    # Update in database
    settings = await db.get_settings(chat_id)
    
    if settings.get("is_muted", False):
        await message.reply_text(
            "ℹ️ **Already Muted**\n\n"
            "Playback is already muted."
        )
        return
    
    settings["is_muted"] = True
    await db.save_settings(chat_id, settings)
    
    await message.reply_text(
        "🔇 **Playback Muted**\n\n"
        "Audio playback has been muted.\n"
        "Use /unmute to resume."
    )

@Client.on_message(filters.command("unmute") & filters.group)
@admin_only
@group_only
@require_voice_chat
@error_handler
@log_command
async def unmute_playback(client: Client, message: Message):
    """Handle /unmute command"""
    
    chat_id = message.chat.id
    
    # Update in database
    settings = await db.get_settings(chat_id)
    
    if not settings.get("is_muted", False):
        await message.reply_text(
            "ℹ️ **Not Muted**\n\n"
            "Playback is not muted."
        )
        return
    
    settings["is_muted"] = False
    await db.save_settings(chat_id, settings)
    
    await message.reply_text(
        "🔊 **Playback Resumed**\n\n"
        "Audio playback has been unmuted."
  )

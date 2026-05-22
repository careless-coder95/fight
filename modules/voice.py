"""
Voice Chat Module
Handles voice chat join/leave commands
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from core.client import client_manager
from core.vc_manager import vc_manager
from utils.decorators import admin_only, group_only, error_handler, log_command

@Client.on_message(filters.command("join") & filters.group)
@admin_only
@group_only
@error_handler
@log_command
async def join_voice_chat(client: Client, message: Message):
    """Handle /join command"""
    
    chat_id = message.chat.id
    
    # Check if already in voice chat
    if vc_manager.is_in_voice_chat(chat_id):
        await message.reply_text(
            "⚠️ **Already Connected**\n\n"
            "Assistant is already in this voice chat!"
        )
        return
    
    # Send processing message
    status_msg = await message.reply_text(
        "🔄 **Connecting to Voice Chat**\n\n"
        "Please wait..."
    )
    
    # Get assistant client
    assistant = client_manager.get_assistant_for_playback()
    
    # Join voice chat
    success = await vc_manager.join_voice_chat(assistant, chat_id)
    
    if success:
        chat_info = vc_manager.get_chat_info(chat_id)
        await status_msg.edit_text(
            "✅ **Successfully Joined Voice Chat**\n\n"
            f"📌 Chat: `{chat_info.get('chat_title', 'Unknown')}`\n"
            f"🎤 Ready to relay audio!"
        )
    else:
        await status_msg.edit_text(
            "❌ **Failed to Join Voice Chat**\n\n"
            "Please make sure:\n"
            "• Voice chat is active\n"
            "• Assistant has proper permissions\n"
            "• Try again in a few seconds"
        )

@Client.on_message(filters.command("leave") & filters.group)
@admin_only
@group_only
@error_handler
@log_command
async def leave_voice_chat(client: Client, message: Message):
    """Handle /leave command"""
    
    chat_id = message.chat.id
    
    # Check if in voice chat
    if not vc_manager.is_in_voice_chat(chat_id):
        await message.reply_text(
            "⚠️ **Not Connected**\n\n"
            "Assistant is not in this voice chat."
        )
        return
    
    # Send processing message
    status_msg = await message.reply_text(
        "🔄 **Leaving Voice Chat**\n\n"
        "Please wait..."
    )
    
    # Get assistant client
    assistant = client_manager.get_assistant_for_playback()
    
    # Leave voice chat
    success = await vc_manager.leave_voice_chat(assistant, chat_id)
    
    if success:
        await status_msg.edit_text(
            "✅ **Successfully Left Voice Chat**\n\n"
            "Assistant has disconnected from voice chat."
        )
    else:
        await status_msg.edit_text(
            "❌ **Failed to Leave Voice Chat**\n\n"
            "An error occurred while leaving."
        )

@Client.on_message(filters.command("leaveall"))
@admin_only
@error_handler
@log_command
async def leave_all_voice_chats(client: Client, message: Message):
    """Handle /leaveall command"""
    
    active_chats = vc_manager.get_active_chats()
    
    if not active_chats:
        await message.reply_text(
            "ℹ️ **No Active Connections**\n\n"
            "Assistant is not connected to any voice chats."
        )
        return
    
    # Send processing message
    status_msg = await message.reply_text(
        f"🔄 **Leaving All Voice Chats**\n\n"
        f"Disconnecting from {len(active_chats)} chat(s)..."
    )
    
    # Get assistant client
    assistant = client_manager.get_assistant_for_playback()
    
    # Leave all chats
    count = await vc_manager.leave_all_voice_chats(assistant)
    
    await status_msg.edit_text(
        f"✅ **Successfully Left All Voice Chats**\n\n"
        f"Disconnected from {count} chat(s)."
)

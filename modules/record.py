"""
Recording Module
Handles voice chat recording commands
"""

import os
from pyrogram import Client, filters
from pyrogram.types import Message
from core.recorder import recorder_manager
from core.vc_manager import vc_manager
from utils.decorators import admin_only, group_only, require_voice_chat, error_handler, log_command
from utils.helpers import get_readable_time, get_readable_size

@Client.on_message(filters.command("startrecord") & filters.group)
@admin_only
@group_only
@require_voice_chat
@error_handler
@log_command
async def start_recording(client: Client, message: Message):
    """Handle /startrecord command"""
    
    chat_id = message.chat.id
    
    # Get or create recorder
    recorder = recorder_manager.create_recorder(chat_id)
    
    # Check if already recording
    if recorder.is_recording:
        status = recorder.get_status()
        duration = int(status.get("duration", 0))
        await message.reply_text(
            "⚠️ **Already Recording**\n\n"
            f"Recording in progress: {get_readable_time(duration)}\n"
            f"Use /stoprecord to stop."
        )
        return
    
    # Send processing message
    status_msg = await message.reply_text(
        "🔄 **Starting Recording**\n\n"
        "Initializing recorder..."
    )
    
    # Start recording (dummy input URL for now - should be connected to actual VC stream)
    # In production, this would be the actual voice chat audio stream
    input_url = "pipe:0"  # Placeholder
    
    success = await recorder.start_recording(input_url)
    
    if success:
        await status_msg.edit_text(
            "⏺ **Recording Started**\n\n"
            "📹 Voice chat is now being recorded.\n"
            "⏱ Use /stoprecord when finished.\n\n"
            "ℹ️ Recording will be automatically uploaded when stopped."
        )
    else:
        await status_msg.edit_text(
            "❌ **Failed to Start Recording**\n\n"
            "An error occurred while starting the recording.\n"
            "Please try again."
        )

@Client.on_message(filters.command("stoprecord") & filters.group)
@admin_only
@group_only
@error_handler
@log_command
async def stop_recording(client: Client, message: Message):
    """Handle /stoprecord command"""
    
    chat_id = message.chat.id
    
    # Get recorder
    recorder = recorder_manager.get_recorder(chat_id)
    
    if not recorder or not recorder.is_recording:
        await message.reply_text(
            "⚠️ **Not Recording**\n\n"
            "No active recording found.\n"
            "Use /startrecord to start recording."
        )
        return
    
    # Send processing message
    status_msg = await message.reply_text(
        "🔄 **Stopping Recording**\n\n"
        "Finalizing recording file..."
    )
    
    # Stop recording
    result = await recorder.stop_recording()
    
    if result:
        duration = result.get("duration", 0)
        file_size = result.get("file_size", 0)
        file_path = result.get("file_path")
        
        await status_msg.edit_text(
            "✅ **Recording Stopped**\n\n"
            f"⏱ Duration: {get_readable_time(int(duration))}\n"
            f"📦 Size: {get_readable_size(file_size)}\n\n"
            "📤 Uploading..."
        )
        
        # Upload recording
        if file_path and os.path.exists(file_path):
            try:
                await message.reply_audio(
                    audio=file_path,
                    caption=(
                        "🎙 **Voice Chat Recording**\n\n"
                        f"⏱ Duration: {get_readable_time(int(duration))}\n"
                        f"📦 Size: {get_readable_size(file_size)}\n"
                        f"📅 Chat: {message.chat.title}"
                    ),
                    duration=int(duration)
                )
                
                await status_msg.delete()
                
                # Delete local file after upload
                try:
                    os.remove(file_path)
                except:
                    pass
                
            except Exception as e:
                await status_msg.edit_text(
                    "❌ **Upload Failed**\n\n"
                    f"Recording saved locally but upload failed.\n"
                    f"Error: {str(e)}"
                )
        else:
            await status_msg.edit_text(
                "❌ **Recording File Not Found**\n\n"
                "The recording was stopped but the file could not be found."
            )
    else:
        await status_msg.edit_text(
            "❌ **Failed to Stop Recording**\n\n"
            "An error occurred while stopping the recording."
  )

"""
Settings Module
Bot settings and configuration commands
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import db
from utils.decorators import admin_only, group_only, error_handler, log_command
from utils.helpers import format_volume_level, format_bass_level

def get_settings_keyboard(chat_id: int, settings: dict) -> InlineKeyboardMarkup:
    """Generate settings keyboard"""
    
    volume = settings.get("volume", 10)
    bass = settings.get("bass_reduction", 5)
    auto_gain = settings.get("auto_gain", True)
    noise_red = settings.get("noise_reduction", False)
    
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"🔊 Volume: {volume}/25",
                callback_data=f"settings_volume_{chat_id}"
            )
        ],
        [
            InlineKeyboardButton(
                f"🎵 Bass Reduction: {bass}/15",
                callback_data=f"settings_bass_{chat_id}"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅' if auto_gain else '❌'} Auto Gain Control",
                callback_data=f"settings_toggle_agc_{chat_id}"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅' if noise_red else '❌'} Noise Reduction",
                callback_data=f"settings_toggle_nr_{chat_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data=f"settings_refresh_{chat_id}"
            ),
            InlineKeyboardButton(
                "❌ Close",
                callback_data=f"settings_close_{chat_id}"
            )
        ]
    ])

@Client.on_message(filters.command("settings") & filters.group)
@admin_only
@group_only
@error_handler
@log_command
async def settings_command(client: Client, message: Message):
    """Handle /settings command"""
    
    chat_id = message.chat.id
    
    # Get current settings
    settings = await db.get_settings(chat_id)
    
    settings_text = (
        "⚙️ **Bot Settings**\n\n"
        f"Configure audio processing settings for this chat.\n\n"
        f"**Current Settings:**\n"
        f"🔊 Volume: `{settings.get('volume', 10)}/25`\n"
        f"🎵 Bass Reduction: `{settings.get('bass_reduction', 5)}/15`\n"
        f"🎚 Auto Gain: `{'Enabled' if settings.get('auto_gain', True) else 'Disabled'}`\n"
        f"🎙 Noise Reduction: `{'Enabled' if settings.get('noise_reduction', False) else 'Disabled'}`"
    )
    
    await message.reply_text(
        settings_text,
        reply_markup=get_settings_keyboard(chat_id, settings)
    )

@Client.on_callback_query(filters.regex(r"^settings_"))
@error_handler
async def settings_callback(client: Client, callback: CallbackQuery):
    """Handle settings callbacks"""
    
    data = callback.data
    parts = data.split("_")
    
    if len(parts) < 3:
        await callback.answer("Invalid callback data")
        return
    
    action = parts[1]
    chat_id = int(parts[2])
    
    # Get current settings
    settings = await db.get_settings(chat_id)
    
    if action == "refresh":
        # Just refresh the display
        settings_text = (
            "⚙️ **Bot Settings**\n\n"
            f"Configure audio processing settings for this chat.\n\n"
            f"**Current Settings:**\n"
            f"🔊 Volume: `{settings.get('volume', 10)}/25`\n"
            f"🎵 Bass Reduction: `{settings.get('bass_reduction', 5)}/15`\n"
            f"🎚 Auto Gain: `{'Enabled' if settings.get('auto_gain', True) else 'Disabled'}`\n"
            f"🎙 Noise Reduction: `{'Enabled' if settings.get('noise_reduction', False) else 'Disabled'}`"
        )
        
        await callback.edit_message_text(
            settings_text,
            reply_markup=get_settings_keyboard(chat_id, settings)
        )
    
    elif action == "toggle":
        toggle_type = parts[2] if len(parts) > 3 else None
        
        if toggle_type == "agc":
            # Toggle Auto Gain Control
            settings["auto_gain"] = not settings.get("auto_gain", True)
            await db.save_settings(chat_id, settings)
            await callback.answer(
                f"Auto Gain Control {'Enabled' if settings['auto_gain'] else 'Disabled'}"
            )
        
        elif toggle_type == "nr":
            # Toggle Noise Reduction
            settings["noise_reduction"] = not settings.get("noise_reduction", False)
            await db.save_settings(chat_id, settings)
            await callback.answer(
                f"Noise Reduction {'Enabled' if settings['noise_reduction'] else 'Disabled'}"
            )
        
        # Refresh display
        settings = await db.get_settings(chat_id)
        settings_text = (
            "⚙️ **Bot Settings**\n\n"
            f"Configure audio processing settings for this chat.\n\n"
            f"**Current Settings:**\n"
            f"🔊 Volume: `{settings.get('volume', 10)}/25`\n"
            f"🎵 Bass Reduction: `{settings.get('bass_reduction', 5)}/15`\n"
            f"🎚 Auto Gain: `{'Enabled' if settings.get('auto_gain', True) else 'Disabled'}`\n"
            f"🎙 Noise Reduction: `{'Enabled' if settings.get('noise_reduction', False) else 'Disabled'}`"
        )
        
        await callback.edit_message_text(
            settings_text,
            reply_markup=get_settings_keyboard(chat_id, settings)
        )
    
    elif action == "volume":
        await callback.answer(
            f"Use /level <1-25> to change volume level\n"
            f"Current: {settings.get('volume', 10)}/25",
            show_alert=True
        )
    
    elif action == "bass":
        await callback.answer(
            f"Use /bass <0-15> to change bass reduction\n"
            f"Current: {settings.get('bass_reduction', 5)}/15",
            show_alert=True
        )
    
    elif action == "close":
        await callback.message.delete()
    
    else:
        await callback.answer("Unknown action")

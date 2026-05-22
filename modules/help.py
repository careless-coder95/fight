"""
Help Module
Provides help and documentation commands
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from core.client import client_manager
from config import BOT_NAME, BOT_VERSION, EMOJI_INFO, EMOJI_SETTINGS
from utils.decorators import error_handler, log_command

# Help text sections
HELP_TEXT = f"""
🎤 **{BOT_NAME}**
Version: `{BOT_VERSION}`

**Realtime Voice Chat Relay & Audio Booster**

This bot captures live voice chat audio, processes it in realtime with volume boosting, bass reduction, and various filters, then rebroadcasts it instantly.

**Key Features:**
• Realtime audio relay with low latency
• Volume boost up to 25 levels
• Bass reduction for voice clarity
• Recording with auto-upload
• Screenshare support
• Dual assistant architecture
"""

COMMANDS_TEXT = """
🎮 **Available Commands**

**Voice Chat:**
• `/join` - Join voice chat
• `/leave` - Leave voice chat
• `/leaveall` - Leave all voice chats

**Audio Control:**
• `/level <1-25>` - Set volume level
• `/bass <0-15>` - Set bass reduction
• `/mute` - Mute playback
• `/unmute` - Unmute playback

**Recording:**
• `/startrecord` - Start recording
• `/stoprecord` - Stop recording

**Screenshare:**
• `/screenshare` - Start screenshare
• `/screenshareoff` - Stop screenshare

**Utilities:**
• `/ping` - Check bot latency
• `/speedtest` - Run speed test
• `/stats` - Show statistics
• `/settings` - Bot settings
• `/help` - Show this help
"""

FEATURES_TEXT = """
✨ **Advanced Features**

**Audio Processing:**
├ Volume Boosting (1-25 levels)
├ Bass Reduction (0-15 levels)
├ Auto Gain Control (AGC)
├ Smart Limiter (anti-clipping)
├ Loudness Normalization
└ Optional Noise Reduction

**Recording:**
├ High quality MP3/WAV
├ Auto upload to Telegram
├ Timestamp filenames
└ Metadata support

**Performance:**
├ uvloop for speed
├ Low latency (<500ms)
├ Async processing
├ Auto recovery
└ Smart buffering
"""

ABOUT_TEXT = f"""
ℹ️ **About {BOT_NAME}**

**Version:** `{BOT_VERSION}`
**Python:** `3.10.19`
**Framework:** Pyrogram

**Architecture:**
This bot uses a dual assistant system with Telegram USER accounts (not bot accounts) for full voice chat functionality.

**How It Works:**
1. Assistant joins voice chat
2. Captures live audio stream
3. Processes with FFmpeg filters
4. Rebroadcasts in realtime
5. Records if requested

**Developer:** @YourUsername
**Support:** @YourSupportChat

Made with ❤️ for the Telegram community
"""

# Inline keyboard
def get_help_keyboard() -> InlineKeyboardMarkup:
    """Get help menu keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Commands", callback_data="help_commands"),
            InlineKeyboardButton("✨ Features", callback_data="help_features"),
        ],
        [
            InlineKeyboardButton(f"{EMOJI_INFO} About", callback_data="help_about"),
            InlineKeyboardButton("❌ Close", callback_data="help_close"),
        ]
    ])

def get_back_keyboard() -> InlineKeyboardMarkup:
    """Get back button keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ Back", callback_data="help_main")]
    ])

@Client.on_message(filters.command("start"))
@error_handler
@log_command
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    
    await message.reply_text(
        HELP_TEXT,
        reply_markup=get_help_keyboard()
    )

@Client.on_message(filters.command("help"))
@error_handler
@log_command
async def help_command(client: Client, message: Message):
    """Handle /help command"""
    
    await message.reply_text(
        HELP_TEXT,
        reply_markup=get_help_keyboard()
    )

@Client.on_callback_query(filters.regex("^help_"))
@error_handler
async def help_callback(client: Client, callback: CallbackQuery):
    """Handle help menu callbacks"""
    
    data = callback.data
    
    if data == "help_main":
        await callback.edit_message_text(
            HELP_TEXT,
            reply_markup=get_help_keyboard()
        )
    
    elif data == "help_commands":
        await callback.edit_message_text(
            COMMANDS_TEXT,
            reply_markup=get_back_keyboard()
        )
    
    elif data == "help_features":
        await callback.edit_message_text(
            FEATURES_TEXT,
            reply_markup=get_back_keyboard()
        )
    
    elif data == "help_about":
        await callback.edit_message_text(
            ABOUT_TEXT,
            reply_markup=get_back_keyboard()
        )
    
    elif data == "help_close":
        await callback.message.delete()
    
    await callback.answer()

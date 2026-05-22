"""
Tools Module
Utility commands like ping, speedtest, stats
"""

import time
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from core.stream_engine import stream_manager
from core.vc_manager import vc_manager
from database import db
from utils.decorators import admin_only, error_handler, log_command
from utils.helpers import get_readable_time, get_system_stats, get_bot_uptime
from config import BOT_NAME, BOT_VERSION

# Bot start time
bot_start_time = time.time()

@Client.on_message(filters.command("ping"))
@error_handler
@log_command
async def ping_command(client: Client, message: Message):
    """Handle /ping command"""
    
    start = time.time()
    sent_msg = await message.reply_text("🏓 Pinging...")
    end = time.time()
    
    latency = round((end - start) * 1000, 2)
    
    await sent_msg.edit_text(
        f"🏓 **Pong!**\n\n"
        f"⚡️ Latency: `{latency}ms`\n"
        f"🤖 Bot is responsive"
    )

@Client.on_message(filters.command("speedtest"))
@admin_only
@error_handler
@log_command
async def speedtest_command(client: Client, message: Message):
    """Handle /speedtest command"""
    
    status_msg = await message.reply_text(
        "🔄 **Running Speed Test**\n\n"
        "Testing connection speed...\n"
        "This may take 30-60 seconds."
    )
    
    try:
        import speedtest
        
        st = speedtest.Speedtest()
        
        # Get best server
        await status_msg.edit_text(
            "🔄 **Running Speed Test**\n\n"
            "Finding best server..."
        )
        st.get_best_server()
        
        # Test download
        await status_msg.edit_text(
            "🔄 **Running Speed Test**\n\n"
            "Testing download speed..."
        )
        download = st.download() / 1_000_000  # Convert to Mbps
        
        # Test upload
        await status_msg.edit_text(
            "🔄 **Running Speed Test**\n\n"
            "Testing upload speed..."
        )
        upload = st.upload() / 1_000_000  # Convert to Mbps
        
        # Get ping
        ping = st.results.ping
        
        # Format results
        result_text = (
            "✅ **Speed Test Results**\n\n"
            f"📥 Download: `{download:.2f} Mbps`\n"
            f"📤 Upload: `{upload:.2f} Mbps`\n"
            f"🏓 Ping: `{ping:.2f} ms`\n\n"
            f"🌐 Server: {st.results.server['sponsor']}\n"
            f"📍 Location: {st.results.server['name']}, {st.results.server['country']}"
        )
        
        await status_msg.edit_text(result_text)
        
    except ImportError:
        await status_msg.edit_text(
            "❌ **Speedtest Not Available**\n\n"
            "The speedtest-cli package is not installed.\n"
            "Install it with: `pip install speedtest-cli`"
        )
    except Exception as e:
        await status_msg.edit_text(
            "❌ **Speed Test Failed**\n\n"
            f"Error: {str(e)}"
        )

@Client.on_message(filters.command("stats"))
@admin_only
@error_handler
@log_command
async def stats_command(client: Client, message: Message):
    """Handle /stats command"""
    
    # Get system stats
    sys_stats = get_system_stats()
    
    # Get voice chat stats
    active_chats = vc_manager.get_active_chats()
    
    # Get stream stats
    all_streams = stream_manager.get_all_stats()
    active_streams = sum(1 for s in all_streams.values() if s.get("is_streaming", False))
    
    # Get database stats
    db_stats = await db.get_stats()
    
    # Format stats
    stats_text = (
        f"📊 **{BOT_NAME} Statistics**\n\n"
        f"**System:**\n"
        f"├ CPU: `{sys_stats['cpu_percent']}%` ({sys_stats['cpu_cores']} cores)\n"
        f"├ RAM: `{sys_stats['memory_percent']}%` ({sys_stats['memory_used']}/{sys_stats['memory_total']})\n"
        f"├ Disk: `{sys_stats['disk_percent']}%` ({sys_stats['disk_used']}/{sys_stats['disk_total']})\n"
        f"└ Uptime: `{get_bot_uptime(bot_start_time)}`\n\n"
        f"**Voice Chats:**\n"
        f"├ Active Connections: `{len(active_chats)}`\n"
        f"├ Active Streams: `{active_streams}`\n"
        f"└ Total Sessions: `{db_stats.get('total_sessions', 0)}`\n\n"
        f"**Bot Info:**\n"
        f"├ Version: `{BOT_VERSION}`\n"
        f"└ Python: `3.10.19`"
    )
    
    await message.reply_text(stats_text)

@Client.on_message(filters.command("status"))
@admin_only
@error_handler
@log_command
async def status_command(client: Client, message: Message):
    """Handle /status command"""
    
    # Get current chat status if in group
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        
        # Check VC status
        is_connected = vc_manager.is_in_voice_chat(chat_id)
        
        # Get stream status
        stream = stream_manager.get_stream(chat_id)
        stream_active = stream and stream.is_streaming if stream else False
        
        # Get settings
        settings = await db.get_settings(chat_id)
        
        status_text = (
            f"📊 **Chat Status**\n\n"
            f"**Voice Chat:**\n"
            f"├ Connected: `{'✅ Yes' if is_connected else '❌ No'}`\n"
            f"└ Streaming: `{'✅ Yes' if stream_active else '❌ No'}`\n\n"
            f"**Audio Settings:**\n"
            f"├ Volume: `{settings.get('volume', 10)}/25`\n"
            f"├ Bass Reduction: `{settings.get('bass_reduction', 5)}/15`\n"
            f"├ Auto Gain: `{'✅' if settings.get('auto_gain', True) else '❌'}`\n"
            f"└ Muted: `{'🔇 Yes' if settings.get('is_muted', False) else '🔊 No'}`"
        )
        
        if stream_active and stream:
            stats = stream.get_stats()
            status_text += (
                f"\n\n**Stream Stats:**\n"
                f"├ Uptime: `{get_readable_time(int(stats['uptime']))}`\n"
                f"├ Packets Sent: `{stats['packets_sent']}`\n"
                f"└ Buffer Health: `{stats['buffer_health']:.1f}%`"
            )
        
        await message.reply_text(status_text)
    else:
        await message.reply_text(
            "ℹ️ **Status Command**\n\n"
            "This command shows chat-specific status.\n"
            "Use it in a group with voice chat."
      )

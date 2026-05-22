#!/usr/bin/env python3
"""
Telegram Realtime Voice Relay & Audio Booster Bot
Advanced voice chat relay system with realtime audio processing

Author: @YourUsername
Version: 2.0.0
Python: 3.10.19
"""

import asyncio
import sys
from pyrogram import idle
from pyrogram.errors import ApiIdInvalid, AuthKeyUnregistered

# Enable uvloop for better performance
try:
    import uvloop
    from config import config
    if config.ENABLE_UVLOOP:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        print("✅ uvloop enabled")
except ImportError:
    print("⚠️  uvloop not available, using default event loop")

from config import config, main_logger, BOT_NAME, BOT_VERSION
from core.client import client_manager
from database import db, cache_cleanup_task
from utils.ffmpeg import ffmpeg_manager

# ANSI Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_banner():
    """Print startup banner"""
    banner = f"""
{CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  {BOLD}{MAGENTA}TELEGRAM REALTIME VOICE RELAY & AUDIO BOOSTER{RESET}{CYAN}      ║
║  {YELLOW}Advanced Voice Chat Processing Engine{RESET}{CYAN}                ║
║                                                           ║
║  {GREEN}Version: {BOT_VERSION}                                      {RESET}{CYAN}║
║  {GREEN}Python: 3.10.19                                        {RESET}{CYAN}║
║  {GREEN}Status: Production Ready                              {RESET}{CYAN}║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

async def startup_checks():
    """Perform startup checks"""
    main_logger.info("🔍 Running startup checks...")
    
    checks_passed = True
    
    # Check configuration
    if not config.validate():
        main_logger.error("❌ Configuration validation failed!")
        checks_passed = False
    else:
        main_logger.info("✅ Configuration validated")
    
    # Check FFmpeg
    if not ffmpeg_manager.is_available():
        main_logger.error("❌ FFmpeg not found! Please install FFmpeg.")
        checks_passed = False
    else:
        version = ffmpeg_manager.get_version()
        main_logger.info(f"✅ {version}")
    
    # Check MongoDB connection
    if not await db.connect():
        main_logger.warning("⚠️  MongoDB connection failed, continuing without database")
    else:
        main_logger.info("✅ MongoDB connected")
    
    return checks_passed

async def load_modules():
    """Load bot modules"""
    try:
        main_logger.info("📦 Loading modules...")
        
        # Import modules (they will auto-register handlers)
        from modules import admin, voice, record, screenshare, tools, settings, help
        
        main_logger.info("✅ All modules loaded")
        return True
        
    except Exception as e:
        main_logger.error(f"❌ Failed to load modules: {e}")
        return False

async def send_startup_message():
    """Send startup notification to log group"""
    try:
        if config.LOG_GROUP_ID:
            startup_text = f"""
🚀 <b>{BOT_NAME}</b> Started!

📊 <b>System Info:</b>
├ Version: <code>{BOT_VERSION}</code>
├ Python: <code>3.10.19</code>
├ FFmpeg: <code>{'✅ Available' if ffmpeg_manager.is_available() else '❌ Not found'}</code>
└ Database: <code>{'✅ Connected' if db.client else '⚠️ Not connected'}</code>

⚙️ <b>Configuration:</b>
├ Mode: <code>{'Dual Assistant' if config.has_dual_assistant() else 'Single Assistant'}</code>
├ Volume: <code>{config.DEFAULT_VOLUME}/{config.MAX_VOLUME}</code>
├ Bass Reduction: <code>{config.DEFAULT_BASS_REDUCTION}</code>
└ Auto Gain: <code>{'✅ Enabled' if config.ENABLE_AUTO_GAIN else '❌ Disabled'}</code>

🎤 <b>Ready to relay voice chats!</b>
"""
            
            await client_manager.bot.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=startup_text
            )
            
            main_logger.info("✅ Startup message sent")
            
    except Exception as e:
        main_logger.error(f"Failed to send startup message: {e}")

async def main():
    """Main bot function"""
    
    print_banner()
    
    try:
        # Startup checks
        if not await startup_checks():
            main_logger.error("❌ Startup checks failed!")
            sys.exit(1)
        
        main_logger.info(f"🚀 Starting {BOT_NAME}...")
        
        # Initialize clients
        await client_manager.initialize()
        
        # Start all clients
        if not await client_manager.start_all():
            main_logger.error("❌ Failed to start clients!")
            sys.exit(1)
        
        # Load modules
        if not await load_modules():
            main_logger.error("❌ Failed to load modules!")
            sys.exit(1)
        
        # Start background tasks
        asyncio.create_task(cache_cleanup_task())
        main_logger.info("✅ Background tasks started")
        
        # Send startup notification
        await send_startup_message()
        
        main_logger.info(f"✅ {BOT_NAME} is now running!")
        main_logger.info("Press Ctrl+C to stop")
        
        # Keep bot running
        await idle()
        
    except ApiIdInvalid:
        main_logger.error("❌ Invalid API_ID or API_HASH!")
        sys.exit(1)
    except AuthKeyUnregistered:
        main_logger.error("❌ Invalid STRING_SESSION!")
        main_logger.error("Generate a new session using: python generate_session.py")
        sys.exit(1)
    except KeyboardInterrupt:
        main_logger.info("\n⚠️  Received shutdown signal")
    except Exception as e:
        main_logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Cleanup
        main_logger.info("🛑 Shutting down...")
        
        try:
            await client_manager.stop_all()
            await db.close()
            main_logger.info("✅ Cleanup completed")
        except Exception as e:
            main_logger.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

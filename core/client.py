"""
Pyrogram Client Manager
Manages bot and assistant clients
"""

from pyrogram import Client
from pyrogram.enums import ParseMode
from typing import Optional
from config import config, main_logger

class ClientManager:
    """Manages Pyrogram clients"""
    
    def __init__(self):
        self.bot: Optional[Client] = None
        self.assistant: Optional[Client] = None
        self.assistant2: Optional[Client] = None
        self.logger = main_logger
    
    async def initialize(self):
        """Initialize all clients"""
        
        # Initialize bot client
        self.bot = Client(
            name="VCRelayBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=ParseMode.HTML,
            in_memory=True
        )
        
        # Initialize assistant client 1
        self.assistant = Client(
            name="VCAssistant1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.STRING_SESSION,
            in_memory=True
        )
        
        # Initialize assistant client 2 if available
        if config.has_dual_assistant():
            self.assistant2 = Client(
                name="VCAssistant2",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=config.STRING_SESSION2,
                in_memory=True
            )
            self.logger.info("✅ Dual assistant mode enabled")
        else:
            self.logger.info("ℹ️ Single assistant mode")
    
    async def start_all(self):
        """Start all clients"""
        try:
            # Start bot
            await self.bot.start()
            me = await self.bot.get_me()
            self.logger.info(f"✅ Bot started: @{me.username}")
            
            # Start assistant 1
            await self.assistant.start()
            assistant_me = await self.assistant.get_me()
            self.logger.info(f"✅ Assistant 1 started: {assistant_me.first_name} (@{assistant_me.username or 'No username'})")
            
            # Start assistant 2 if available
            if self.assistant2:
                await self.assistant2.start()
                assistant2_me = await self.assistant2.get_me()
                self.logger.info(f"✅ Assistant 2 started: {assistant2_me.first_name} (@{assistant2_me.username or 'No username'})")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start clients: {e}")
            return False
    
    async def stop_all(self):
        """Stop all clients"""
        try:
            if self.bot:
                await self.bot.stop()
                self.logger.info("Bot stopped")
            
            if self.assistant:
                await self.assistant.stop()
                self.logger.info("Assistant 1 stopped")
            
            if self.assistant2:
                await self.assistant2.stop()
                self.logger.info("Assistant 2 stopped")
                
        except Exception as e:
            self.logger.error(f"Error stopping clients: {e}")
    
    def get_assistant_for_recording(self) -> Client:
        """Get assistant client for recording"""
        return self.assistant
    
    def get_assistant_for_playback(self) -> Client:
        """Get assistant client for playback"""
        # Use assistant2 if available, otherwise use assistant1
        return self.assistant2 if self.assistant2 else self.assistant
    
    async def get_bot_info(self) -> dict:
        """Get bot information"""
        try:
            me = await self.bot.get_me()
            return {
                "id": me.id,
                "username": me.username,
                "first_name": me.first_name,
                "is_bot": me.is_bot,
            }
        except Exception as e:
            self.logger.error(f"Error getting bot info: {e}")
            return {}
    
    async def get_assistant_info(self, assistant_num: int = 1) -> dict:
        """Get assistant information"""
        try:
            client = self.assistant if assistant_num == 1 else self.assistant2
            if not client:
                return {}
            
            me = await client.get_me()
            return {
                "id": me.id,
                "username": me.username,
                "first_name": me.first_name,
                "last_name": me.last_name,
            }
        except Exception as e:
            self.logger.error(f"Error getting assistant info: {e}")
            return {}

# Global client manager
client_manager = ClientManager()

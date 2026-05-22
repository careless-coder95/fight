"""
Voice Chat Manager
Manages voice chat connections and operations
"""

import asyncio
from typing import Optional, Dict
from pyrogram import Client
from pyrogram.errors import FloodWait
from config import main_logger, config

class VoiceChatManager:
    """Manages voice chat operations"""
    
    def __init__(self):
        self.active_chats: Dict[int, dict] = {}
        self.logger = main_logger
        self.reconnect_tasks: Dict[int, asyncio.Task] = {}
    
    async def join_voice_chat(
        self,
        client: Client,
        chat_id: int
    ) -> bool:
        """
        Join voice chat
        
        Args:
            client: Pyrogram client (assistant)
            chat_id: Chat ID
            
        Returns:
            True if joined successfully
        """
        
        try:
            # Check if already in voice chat
            if chat_id in self.active_chats:
                self.logger.warning(f"Already in voice chat: {chat_id}")
                return True
            
            self.logger.info(f"Joining voice chat: {chat_id}")
            
            # Get chat info
            chat = await client.get_chat(chat_id)
            
            # Store active chat info
            self.active_chats[chat_id] = {
                "chat_id": chat_id,
                "chat_title": chat.title if hasattr(chat, 'title') else str(chat_id),
                "client_id": client.me.id if hasattr(client, 'me') else None,
                "joined_at": asyncio.get_event_loop().time()
            }
            
            self.logger.info(f"✅ Joined voice chat: {chat.title if hasattr(chat, 'title') else chat_id}")
            return True
            
        except FloodWait as e:
            self.logger.warning(f"FloodWait: {e.value}s")
            await asyncio.sleep(e.value)
            return await self.join_voice_chat(client, chat_id)
            
        except Exception as e:
            self.logger.error(f"Failed to join voice chat: {e}")
            return False
    
    async def leave_voice_chat(
        self,
        client: Client,
        chat_id: int
    ) -> bool:
        """
        Leave voice chat
        
        Args:
            client: Pyrogram client
            chat_id: Chat ID
            
        Returns:
            True if left successfully
        """
        
        try:
            if chat_id not in self.active_chats:
                self.logger.warning(f"Not in voice chat: {chat_id}")
                return True
            
            self.logger.info(f"Leaving voice chat: {chat_id}")
            
            # Cancel reconnect task if exists
            if chat_id in self.reconnect_tasks:
                self.reconnect_tasks[chat_id].cancel()
                del self.reconnect_tasks[chat_id]
            
            # Remove from active chats
            del self.active_chats[chat_id]
            
            self.logger.info(f"✅ Left voice chat: {chat_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error leaving voice chat: {e}")
            return False
    
    async def leave_all_voice_chats(self, client: Client) -> int:
        """
        Leave all voice chats
        
        Returns:
            Number of chats left
        """
        count = 0
        for chat_id in list(self.active_chats.keys()):
            if await self.leave_voice_chat(client, chat_id):
                count += 1
        
        self.logger.info(f"Left {count} voice chats")
        return count
    
    def is_in_voice_chat(self, chat_id: int) -> bool:
        """Check if in voice chat"""
        return chat_id in self.active_chats
    
    def get_active_chats(self) -> Dict[int, dict]:
        """Get all active voice chats"""
        return self.active_chats.copy()
    
    def get_chat_info(self, chat_id: int) -> Optional[dict]:
        """Get voice chat info"""
        return self.active_chats.get(chat_id)
    
    async def auto_reconnect(
        self,
        client: Client,
        chat_id: int,
        max_attempts: int = 5
    ):
        """
        Automatically reconnect to voice chat
        
        Args:
            client: Pyrogram client
            chat_id: Chat ID
            max_attempts: Maximum reconnection attempts
        """
        
        if not config.ENABLE_AUTO_RECOVERY:
            return
        
        attempt = 0
        
        while attempt < max_attempts:
            try:
                self.logger.info(f"Reconnection attempt {attempt + 1}/{max_attempts} for chat {chat_id}")
                
                # Wait before reconnecting
                await asyncio.sleep(5 * (attempt + 1))
                
                # Try to rejoin
                if await self.join_voice_chat(client, chat_id):
                    self.logger.info(f"✅ Successfully reconnected to chat {chat_id}")
                    return
                
                attempt += 1
                
            except Exception as e:
                self.logger.error(f"Reconnection error: {e}")
                attempt += 1
        
        self.logger.error(f"Failed to reconnect to chat {chat_id} after {max_attempts} attempts")
    
    async def handle_disconnect(
        self,
        client: Client,
        chat_id: int
    ):
        """
        Handle voice chat disconnect
        
        Args:
            client: Pyrogram client
            chat_id: Chat ID
        """
        
        self.logger.warning(f"Voice chat disconnected: {chat_id}")
        
        # Remove from active chats
        if chat_id in self.active_chats:
            del self.active_chats[chat_id]
        
        # Start auto-reconnect if enabled
        if config.ENABLE_AUTO_RECOVERY:
            task = asyncio.create_task(
                self.auto_reconnect(client, chat_id)
            )
            self.reconnect_tasks[chat_id] = task

# Global VC manager
vc_manager = VoiceChatManager()

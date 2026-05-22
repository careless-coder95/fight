"""
MongoDB Database Handler
Manages database connections and operations
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from typing import Optional, Dict, Any, List
from config import config, main_logger

class MongoDB:
    """MongoDB database manager"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.logger = main_logger
        
    async def connect(self) -> bool:
        """
        Connect to MongoDB
        
        Returns:
            True if connected successfully
        """
        try:
            self.client = AsyncIOMotorClient(config.MONGO_URL)
            self.db = self.client[config.MONGO_DB_NAME]
            
            # Test connection
            await self.client.admin.command('ping')
            
            self.logger.info(f"✅ Connected to MongoDB: {config.MONGO_DB_NAME}")
            return True
            
        except ConnectionFailure as e:
            self.logger.error(f"❌ MongoDB connection failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ MongoDB error: {e}")
            return False
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed")
    
    # Chat Management
    async def add_chat(self, chat_id: int, chat_data: Dict[str, Any]) -> bool:
        """Add or update chat"""
        try:
            await self.db.chats.update_one(
                {"chat_id": chat_id},
                {"$set": chat_data},
                upsert=True
            )
            return True
        except Exception as e:
            self.logger.error(f"Error adding chat: {e}")
            return False
    
    async def get_chat(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Get chat data"""
        try:
            return await self.db.chats.find_one({"chat_id": chat_id})
        except Exception as e:
            self.logger.error(f"Error getting chat: {e}")
            return None
    
    async def remove_chat(self, chat_id: int) -> bool:
        """Remove chat"""
        try:
            await self.db.chats.delete_one({"chat_id": chat_id})
            return True
        except Exception as e:
            self.logger.error(f"Error removing chat: {e}")
            return False
    
    async def get_all_chats(self) -> List[Dict[str, Any]]:
        """Get all chats"""
        try:
            cursor = self.db.chats.find({})
            return await cursor.to_list(length=None)
        except Exception as e:
            self.logger.error(f"Error getting all chats: {e}")
            return []
    
    # Settings Management
    async def save_settings(self, chat_id: int, settings: Dict[str, Any]) -> bool:
        """Save chat settings"""
        try:
            await self.db.settings.update_one(
                {"chat_id": chat_id},
                {"$set": settings},
                upsert=True
            )
            return True
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            return False
    
    async def get_settings(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Get chat settings"""
        try:
            settings = await self.db.settings.find_one({"chat_id": chat_id})
            
            # Return default settings if not found
            if not settings:
                default_settings = {
                    "chat_id": chat_id,
                    "volume": config.DEFAULT_VOLUME,
                    "bass_reduction": config.DEFAULT_BASS_REDUCTION,
                    "auto_gain": config.ENABLE_AUTO_GAIN,
                    "noise_reduction": config.ENABLE_NOISE_REDUCTION,
                }
                await self.save_settings(chat_id, default_settings)
                return default_settings
            
            return settings
            
        except Exception as e:
            self.logger.error(f"Error getting settings: {e}")
            return None
    
    # Statistics
    async def update_stats(self, stat_type: str, increment: int = 1) -> bool:
        """Update statistics"""
        try:
            await self.db.stats.update_one(
                {"type": stat_type},
                {"$inc": {"count": increment}},
                upsert=True
            )
            return True
        except Exception as e:
            self.logger.error(f"Error updating stats: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, int]:
        """Get all statistics"""
        try:
            cursor = self.db.stats.find({})
            stats_list = await cursor.to_list(length=None)
            
            stats = {}
            for stat in stats_list:
                stats[stat['type']] = stat.get('count', 0)
            
            return stats
        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {}
    
    # Recording Management
    async def save_recording(self, recording_data: Dict[str, Any]) -> bool:
        """Save recording metadata"""
        try:
            await self.db.recordings.insert_one(recording_data)
            return True
        except Exception as e:
            self.logger.error(f"Error saving recording: {e}")
            return False
    
    async def get_recordings(self, chat_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recordings for a chat"""
        try:
            cursor = self.db.recordings.find(
                {"chat_id": chat_id}
            ).sort("timestamp", -1).limit(limit)
            
            return await cursor.to_list(length=limit)
        except Exception as e:
            self.logger.error(f"Error getting recordings: {e}")
            return []

# Global database instance
db = MongoDB()

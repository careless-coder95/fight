"""
In-Memory Cache
Fast caching layer for frequently accessed data
"""

import asyncio
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
from config import main_logger

class Cache:
    """In-memory cache with TTL support"""
    
    def __init__(self, default_ttl: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self.logger = main_logger
        self._lock = asyncio.Lock()
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set cache value
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful
        """
        try:
            async with self._lock:
                expiry = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
                self._cache[key] = {
                    "value": value,
                    "expiry": expiry
                }
                return True
        except Exception as e:
            self.logger.error(f"Cache set error: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get cache value
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        try:
            async with self._lock:
                if key not in self._cache:
                    return None
                
                cache_entry = self._cache[key]
                
                # Check expiry
                if datetime.now() > cache_entry["expiry"]:
                    del self._cache[key]
                    return None
                
                return cache_entry["value"]
                
        except Exception as e:
            self.logger.error(f"Cache get error: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """Delete cache entry"""
        try:
            async with self._lock:
                if key in self._cache:
                    del self._cache[key]
                return True
        except Exception as e:
            self.logger.error(f"Cache delete error: {e}")
            return False
    
    async def clear(self) -> bool:
        """Clear all cache"""
        try:
            async with self._lock:
                self._cache.clear()
                return True
        except Exception as e:
            self.logger.error(f"Cache clear error: {e}")
            return False
    
    async def cleanup_expired(self):
        """Remove expired entries"""
        try:
            async with self._lock:
                now = datetime.now()
                expired_keys = [
                    key for key, entry in self._cache.items()
                    if now > entry["expiry"]
                ]
                
                for key in expired_keys:
                    del self._cache[key]
                
                if expired_keys:
                    self.logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
                    
        except Exception as e:
            self.logger.error(f"Cache cleanup error: {e}")
    
    async def get_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        async with self._lock:
            return {
                "total_entries": len(self._cache),
                "expired_entries": sum(
                    1 for entry in self._cache.values()
                    if datetime.now() > entry["expiry"]
                )
            }

# Global cache instance
cache = Cache()

# Periodic cleanup task
async def cache_cleanup_task():
    """Background task to cleanup expired cache entries"""
    while True:
        await asyncio.sleep(300)  # Run every 5 minutes
        await cache.cleanup_expired()

"""
Configuration Settings
Loads and validates environment variables
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Bot configuration"""
    
    # Telegram API
    API_ID: int = int(os.getenv("API_ID", "0"))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Assistant Accounts
    STRING_SESSION: str = os.getenv("STRING_SESSION", "")
    STRING_SESSION2: Optional[str] = os.getenv("STRING_SESSION2", None)
    
    # MongoDB
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "telegram_vc_relay")
    
    # Admin
    LOG_GROUP_ID: int = int(os.getenv("LOG_GROUP_ID", "0"))
    SUDO_USERS: List[int] = [
        int(x) for x in os.getenv("SUDO_USERS", "").split(",") if x.strip()
    ]
    
    # Bot Info
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "")
    ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "VC Relay Assistant")
    ASSISTANT_NAME2: str = os.getenv("ASSISTANT_NAME2", "VC Relay Assistant 2")
    
    # Audio Configuration
    DEFAULT_VOLUME: int = int(os.getenv("DEFAULT_VOLUME", "10"))
    MAX_VOLUME: int = int(os.getenv("MAX_VOLUME", "25"))
    DEFAULT_BASS_REDUCTION: int = int(os.getenv("DEFAULT_BASS_REDUCTION", "5"))
    SAMPLE_RATE: int = int(os.getenv("SAMPLE_RATE", "48000"))
    CHANNELS: int = int(os.getenv("CHANNELS", "2"))
    BITRATE: str = os.getenv("BITRATE", "128k")
    
    # Stream Configuration
    STREAM_BUFFER_SIZE: int = int(os.getenv("STREAM_BUFFER_SIZE", "65536"))
    MAX_LATENCY_MS: int = int(os.getenv("MAX_LATENCY_MS", "500"))
    ENABLE_UVLOOP: bool = os.getenv("ENABLE_UVLOOP", "true").lower() == "true"
    
    # Recording Configuration
    RECORDING_FORMAT: str = os.getenv("RECORDING_FORMAT", "mp3")
    RECORDING_QUALITY: str = os.getenv("RECORDING_QUALITY", "320")
    
    # Screenshare Configuration
    SCREEN_WIDTH: int = int(os.getenv("SCREEN_WIDTH", "1920"))
    SCREEN_HEIGHT: int = int(os.getenv("SCREEN_HEIGHT", "1080"))
    SCREEN_FPS: int = int(os.getenv("SCREEN_FPS", "30"))
    
    # Advanced Settings
    ENABLE_AUTO_RECOVERY: bool = os.getenv("ENABLE_AUTO_RECOVERY", "true").lower() == "true"
    ENABLE_NOISE_REDUCTION: bool = os.getenv("ENABLE_NOISE_REDUCTION", "false").lower() == "true"
    ENABLE_AUTO_GAIN: bool = os.getenv("ENABLE_AUTO_GAIN", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required = [
            ("API_ID", cls.API_ID),
            ("API_HASH", cls.API_HASH),
            ("BOT_TOKEN", cls.BOT_TOKEN),
            ("STRING_SESSION", cls.STRING_SESSION),
        ]
        
        missing = []
        for name, value in required:
            if not value or (isinstance(value, int) and value == 0):
                missing.append(name)
        
        if missing:
            print(f"❌ Missing required configuration: {', '.join(missing)}")
            return False
        
        return True
    
    @classmethod
    def has_dual_assistant(cls) -> bool:
        """Check if dual assistant mode is enabled"""
        return bool(cls.STRING_SESSION2)

# Export config instance
config = Config()

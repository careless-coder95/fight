"""
Data Models
Defines data structures for the bot
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class ChatSession:
    """Voice chat session data"""
    chat_id: int
    chat_title: str
    is_active: bool = False
    is_recording: bool = False
    is_screenshare: bool = False
    is_muted: bool = False
    volume: int = 10
    bass_reduction: int = 5
    joined_at: Optional[datetime] = None
    assistant_id: Optional[int] = None
    assistant2_id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "chat_id": self.chat_id,
            "chat_title": self.chat_title,
            "is_active": self.is_active,
            "is_recording": self.is_recording,
            "is_screenshare": self.is_screenshare,
            "is_muted": self.is_muted,
            "volume": self.volume,
            "bass_reduction": self.bass_reduction,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "assistant_id": self.assistant_id,
            "assistant2_id": self.assistant2_id,
        }

@dataclass
class StreamConfig:
    """Stream configuration"""
    sample_rate: int = 48000
    channels: int = 2
    bitrate: str = "128k"
    buffer_size: int = 65536
    volume: float = 1.0
    bass_reduction: int = 5
    enable_auto_gain: bool = True
    enable_noise_reduction: bool = False
    enable_limiter: bool = True
    
    def get_ffmpeg_filters(self) -> str:
        """Generate FFmpeg filter string"""
        filters = []
        
        # Volume control
        if self.volume != 1.0:
            filters.append(f"volume={self.volume}")
        
        # Bass reduction (highpass filter)
        if self.bass_reduction > 0:
            cutoff_freq = 80 + (self.bass_reduction * 10)
            filters.append(f"highpass=f={cutoff_freq}")
        
        # Auto gain control
        if self.enable_auto_gain:
            filters.append("loudnorm=I=-16:TP=-1.5:LRA=11")
        
        # Noise reduction
        if self.enable_noise_reduction:
            filters.append("afftdn=nf=-25")
        
        # Limiter to prevent clipping
        if self.enable_limiter:
            filters.append("alimiter=limit=0.9:attack=5:release=50")
        
        return ",".join(filters) if filters else None

@dataclass
class RecordingData:
    """Recording metadata"""
    chat_id: int
    filename: str
    duration: float
    file_size: int
    format: str
    timestamp: datetime = field(default_factory=datetime.now)
    file_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "chat_id": self.chat_id,
            "filename": self.filename,
            "duration": self.duration,
            "file_size": self.file_size,
            "format": self.format,
            "timestamp": self.timestamp.isoformat(),
            "file_id": self.file_id,
        }

@dataclass
class StreamStats:
    """Stream statistics"""
    packets_sent: int = 0
    packets_received: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    latency_ms: float = 0.0
    buffer_health: float = 100.0
    dropped_packets: int = 0
    started_at: datetime = field(default_factory=datetime.now)
    
    def get_uptime(self) -> float:
        """Get uptime in seconds"""
        return (datetime.now() - self.started_at).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "packets_sent": self.packets_sent,
            "packets_received": self.packets_received,
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
            "latency_ms": self.latency_ms,
            "buffer_health": self.buffer_health,
            "dropped_packets": self.dropped_packets,
            "uptime": self.get_uptime(),
        }

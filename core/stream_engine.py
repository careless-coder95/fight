"""
Stream Engine
Handles realtime audio streaming and processing
"""

import asyncio
import subprocess
from typing import Optional, Dict
from datetime import datetime
from config import stream_logger, config
from database import StreamStats
from utils.ffmpeg import ffmpeg_manager

class StreamEngine:
    """Realtime audio stream processor"""
    
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.logger = stream_logger
        self.process: Optional[subprocess.Popen] = None
        self.is_streaming = False
        self.stats = StreamStats()
        
        # Stream configuration
        self.volume = config.DEFAULT_VOLUME / 10  # Convert to multiplier
        self.bass_reduction = config.DEFAULT_BASS_REDUCTION
        self.enable_auto_gain = config.ENABLE_AUTO_GAIN
        
    async def start_stream(
        self,
        input_url: str,
        output_url: str
    ) -> bool:
        """
        Start audio stream processing
        
        Args:
            input_url: Input audio stream URL/pipe
            output_url: Output audio stream URL/pipe
            
        Returns:
            True if started successfully
        """
        
        try:
            if self.is_streaming:
                self.logger.warning(f"Stream already running for chat {self.chat_id}")
                return False
            
            # Build FFmpeg command
            cmd = ffmpeg_manager.build_relay_command(
                input_url=input_url,
                output_url=output_url,
                volume=self.volume,
                bass_reduction=self.bass_reduction,
                enable_auto_gain=self.enable_auto_gain,
                enable_limiter=True
            )
            
            self.logger.info(f"Starting stream for chat {self.chat_id}")
            self.logger.debug(f"FFmpeg command: {' '.join(cmd)}")
            
            # Start FFmpeg process
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=config.STREAM_BUFFER_SIZE
            )
            
            self.is_streaming = True
            self.stats.started_at = datetime.now()
            
            # Monitor process
            asyncio.create_task(self._monitor_process())
            
            self.logger.info(f"✅ Stream started for chat {self.chat_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start stream: {e}")
            return False
    
    async def stop_stream(self) -> bool:
        """Stop audio stream"""
        try:
            if not self.is_streaming:
                return True
            
            self.logger.info(f"Stopping stream for chat {self.chat_id}")
            
            if self.process:
                self.process.terminate()
                
                # Wait for process to terminate
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.logger.warning("Force killed FFmpeg process")
            
            self.is_streaming = False
            self.logger.info(f"✅ Stream stopped for chat {self.chat_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping stream: {e}")
            return False
    
    async def update_volume(self, level: int) -> bool:
        """
        Update volume level (requires stream restart)
        
        Args:
            level: Volume level (1-25)
            
        Returns:
            True if updated successfully
        """
        try:
            self.volume = level / 10
            self.logger.info(f"Volume updated to {level} for chat {self.chat_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating volume: {e}")
            return False
    
    async def update_bass_reduction(self, level: int) -> bool:
        """
        Update bass reduction level (requires stream restart)
        
        Args:
            level: Bass reduction level (0-15)
            
        Returns:
            True if updated successfully
        """
        try:
            self.bass_reduction = level
            self.logger.info(f"Bass reduction updated to {level} for chat {self.chat_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating bass reduction: {e}")
            return False
    
    async def _monitor_process(self):
        """Monitor FFmpeg process and collect stats"""
        while self.is_streaming and self.process:
            try:
                # Check if process is alive
                if self.process.poll() is not None:
                    self.logger.error(f"FFmpeg process died for chat {self.chat_id}")
                    self.is_streaming = False
                    
                    # Log stderr
                    if self.process.stderr:
                        stderr = self.process.stderr.read()
                        if stderr:
                            self.logger.error(f"FFmpeg stderr: {stderr.decode()}")
                    break
                
                # Update stats
                self.stats.packets_sent += 1
                
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error monitoring process: {e}")
                break
    
    def get_stats(self) -> Dict:
        """Get stream statistics"""
        return {
            "is_streaming": self.is_streaming,
            "uptime": self.stats.get_uptime() if self.is_streaming else 0,
            "volume": self.volume * 10,
            "bass_reduction": self.bass_reduction,
            **self.stats.to_dict()
        }
    
    def __del__(self):
        """Cleanup on deletion"""
        if self.is_streaming:
            asyncio.create_task(self.stop_stream())

class StreamManager:
    """Manages multiple stream engines"""
    
    def __init__(self):
        self.streams: Dict[int, StreamEngine] = {}
        self.logger = stream_logger
    
    def create_stream(self, chat_id: int) -> StreamEngine:
        """Create or get stream engine for chat"""
        if chat_id not in self.streams:
            self.streams[chat_id] = StreamEngine(chat_id)
            self.logger.info(f"Created stream engine for chat {chat_id}")
        
        return self.streams[chat_id]
    
    def get_stream(self, chat_id: int) -> Optional[StreamEngine]:
        """Get stream engine for chat"""
        return self.streams.get(chat_id)
    
    async def remove_stream(self, chat_id: int) -> bool:
        """Remove stream engine"""
        if chat_id in self.streams:
            stream = self.streams[chat_id]
            await stream.stop_stream()
            del self.streams[chat_id]
            self.logger.info(f"Removed stream engine for chat {chat_id}")
            return True
        return False
    
    async def stop_all_streams(self):
        """Stop all active streams"""
        for chat_id, stream in list(self.streams.items()):
            await stream.stop_stream()
        self.streams.clear()
        self.logger.info("All streams stopped")
    
    def get_all_stats(self) -> Dict[int, Dict]:
        """Get statistics for all streams"""
        return {
            chat_id: stream.get_stats()
            for chat_id, stream in self.streams.items()
        }

# Global stream manager
stream_manager = StreamManager()

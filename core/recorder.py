"""
Voice Chat Recorder
Handles VC recording functionality
"""

import asyncio
import os
from typing import Optional
from datetime import datetime
from pathlib import Path
from config import main_logger, config
from database import RecordingData, db
from utils.ffmpeg import ffmpeg_manager

class Recorder:
    """Voice chat recorder"""
    
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.logger = main_logger
        self.is_recording = False
        self.process: Optional[asyncio.subprocess.Process] = None
        self.output_file: Optional[str] = None
        self.start_time: Optional[datetime] = None
        
        # Create recordings directory
        self.recordings_dir = Path("recordings")
        self.recordings_dir.mkdir(exist_ok=True)
    
    async def start_recording(
        self,
        input_url: str,
        format: str = None,
        quality: str = None
    ) -> bool:
        """
        Start recording voice chat
        
        Args:
            input_url: Input audio stream URL
            format: Output format (mp3, wav, ogg)
            quality: Audio quality/bitrate
            
        Returns:
            True if started successfully
        """
        
        try:
            if self.is_recording:
                self.logger.warning(f"Already recording for chat {self.chat_id}")
                return False
            
            # Use config defaults if not specified
            format = format or config.RECORDING_FORMAT
            quality = quality or config.RECORDING_QUALITY
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{self.chat_id}_{timestamp}.{format}"
            self.output_file = str(self.recordings_dir / filename)
            
            # Build FFmpeg command
            cmd = ffmpeg_manager.build_recording_command(
                input_url=input_url,
                output_file=self.output_file,
                format=format,
                quality=quality
            )
            
            self.logger.info(f"Starting recording for chat {self.chat_id}")
            self.logger.debug(f"Output file: {self.output_file}")
            
            # Start recording process
            self.process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.is_recording = True
            self.start_time = datetime.now()
            
            self.logger.info(f"✅ Recording started: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            return False
    
    async def stop_recording(self) -> Optional[dict]:
        """
        Stop recording
        
        Returns:
            Recording metadata dict or None
        """
        
        try:
            if not self.is_recording:
                self.logger.warning(f"Not recording for chat {self.chat_id}")
                return None
            
            self.logger.info(f"Stopping recording for chat {self.chat_id}")
            
            # Terminate FFmpeg process
            if self.process:
                self.process.terminate()
                
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    self.process.kill()
                    self.logger.warning("Force killed recording process")
            
            self.is_recording = False
            
            # Calculate duration
            duration = 0.0
            if self.start_time:
                duration = (datetime.now() - self.start_time).total_seconds()
            
            # Get file size
            file_size = 0
            if self.output_file and os.path.exists(self.output_file):
                file_size = os.path.getsize(self.output_file)
            
            # Create recording data
            recording_data = RecordingData(
                chat_id=self.chat_id,
                filename=os.path.basename(self.output_file),
                duration=duration,
                file_size=file_size,
                format=config.RECORDING_FORMAT
            )
            
            # Save to database
            await db.save_recording(recording_data.to_dict())
            
            self.logger.info(f"✅ Recording stopped: {recording_data.filename}")
            self.logger.info(f"Duration: {duration:.1f}s, Size: {file_size / 1024 / 1024:.2f} MB")
            
            return {
                "file_path": self.output_file,
                "filename": recording_data.filename,
                "duration": duration,
                "file_size": file_size,
                "format": recording_data.format
            }
            
        except Exception as e:
            self.logger.error(f"Error stopping recording: {e}")
            return None
    
    def get_status(self) -> dict:
        """Get recording status"""
        status = {
            "is_recording": self.is_recording,
            "output_file": self.output_file,
        }
        
        if self.is_recording and self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            status["duration"] = duration
        
        return status
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.is_recording:
            await self.stop_recording()

class RecorderManager:
    """Manages multiple recorders"""
    
    def __init__(self):
        self.recorders: dict[int, Recorder] = {}
        self.logger = main_logger
    
    def create_recorder(self, chat_id: int) -> Recorder:
        """Create or get recorder for chat"""
        if chat_id not in self.recorders:
            self.recorders[chat_id] = Recorder(chat_id)
            self.logger.info(f"Created recorder for chat {chat_id}")
        
        return self.recorders[chat_id]
    
    def get_recorder(self, chat_id: int) -> Optional[Recorder]:
        """Get recorder for chat"""
        return self.recorders.get(chat_id)
    
    async def remove_recorder(self, chat_id: int) -> bool:
        """Remove recorder"""
        if chat_id in self.recorders:
            recorder = self.recorders[chat_id]
            await recorder.cleanup()
            del self.recorders[chat_id]
            self.logger.info(f"Removed recorder for chat {chat_id}")
            return True
        return False
    
    async def stop_all_recordings(self):
        """Stop all active recordings"""
        for chat_id, recorder in list(self.recorders.items()):
            if recorder.is_recording:
                await recorder.stop_recording()
        
        self.logger.info("All recordings stopped")
    
    def get_all_status(self) -> dict[int, dict]:
        """Get status for all recorders"""
        return {
            chat_id: recorder.get_status()
            for chat_id, recorder in self.recorders.items()
        }

# Global recorder manager
recorder_manager = RecorderManager()

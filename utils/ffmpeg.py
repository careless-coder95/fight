"""
FFmpeg Utilities
Handles FFmpeg operations and filter generation
"""

import asyncio
import subprocess
import shutil
from typing import Optional, List
from config import config, ffmpeg_logger

class FFmpegManager:
    """FFmpeg operations manager"""
    
    def __init__(self):
        self.logger = ffmpeg_logger
        self.ffmpeg_path = shutil.which("ffmpeg")
        
        if not self.ffmpeg_path:
            self.logger.error("❌ FFmpeg not found in PATH!")
    
    def is_available(self) -> bool:
        """Check if FFmpeg is available"""
        return self.ffmpeg_path is not None
    
    def build_relay_command(
        self,
        input_url: str,
        output_url: str,
        volume: float = 1.0,
        bass_reduction: int = 5,
        enable_auto_gain: bool = True,
        enable_limiter: bool = True,
    ) -> List[str]:
        """
        Build FFmpeg command for realtime audio relay
        
        Args:
            input_url: Input audio stream URL
            output_url: Output stream URL
            volume: Volume multiplier
            bass_reduction: Bass reduction level (0-15)
            enable_auto_gain: Enable automatic gain control
            enable_limiter: Enable audio limiter
            
        Returns:
            FFmpeg command as list
        """
        
        # Build filter chain
        filters = []
        
        # Volume control
        if volume != 1.0:
            filters.append(f"volume={volume}")
        
        # Bass reduction (highpass filter)
        if bass_reduction > 0:
            cutoff_freq = 80 + (bass_reduction * 10)
            filters.append(f"highpass=f={cutoff_freq}")
        
        # Auto gain control (loudness normalization)
        if enable_auto_gain:
            filters.append("loudnorm=I=-16:TP=-1.5:LRA=11:linear=true")
        
        # Limiter to prevent clipping
        if enable_limiter:
            filters.append("alimiter=limit=0.9:attack=5:release=50")
        
        filter_complex = ",".join(filters) if filters else None
        
        # Build command
        cmd = [
            self.ffmpeg_path,
            "-re",  # Read input at native frame rate
            "-i", input_url,
            "-f", "s16le",  # Output format
            "-ar", str(config.SAMPLE_RATE),  # Sample rate
            "-ac", str(config.CHANNELS),  # Audio channels
        ]
        
        # Add filter complex if any
        if filter_complex:
            cmd.extend(["-af", filter_complex])
        
        # Output options
        cmd.extend([
            "-bufsize", str(config.STREAM_BUFFER_SIZE),
            output_url
        ])
        
        return cmd
    
    def build_recording_command(
        self,
        input_url: str,
        output_file: str,
        format: str = "mp3",
        quality: str = "320k"
    ) -> List[str]:
        """
        Build FFmpeg command for recording
        
        Args:
            input_url: Input audio stream URL
            output_file: Output file path
            format: Output format (mp3, wav, etc.)
            quality: Audio quality/bitrate
            
        Returns:
            FFmpeg command as list
        """
        
        cmd = [
            self.ffmpeg_path,
            "-i", input_url,
            "-ar", str(config.SAMPLE_RATE),
            "-ac", str(config.CHANNELS),
        ]
        
        # Format-specific options
        if format == "mp3":
            cmd.extend([
                "-codec:a", "libmp3lame",
                "-b:a", quality,
                "-q:a", "0"
            ])
        elif format == "wav":
            cmd.extend([
                "-codec:a", "pcm_s16le"
            ])
        elif format == "ogg":
            cmd.extend([
                "-codec:a", "libvorbis",
                "-q:a", "10"
            ])
        
        cmd.append(output_file)
        
        return cmd
    
    def build_screenshare_command(
        self,
        output_url: str,
        width: int = 1920,
        height: int = 1080,
        fps: int = 30,
        display: str = ":0"
    ) -> List[str]:
        """
        Build FFmpeg command for screenshare
        
        Args:
            output_url: Output stream URL
            width: Screen width
            height: Screen height
            fps: Frames per second
            display: X11 display
            
        Returns:
            FFmpeg command as list
        """
        
        cmd = [
            self.ffmpeg_path,
            "-f", "x11grab",
            "-video_size", f"{width}x{height}",
            "-framerate", str(fps),
            "-i", display,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-pix_fmt", "yuv420p",
            "-f", "rawvideo",
            output_url
        ]
        
        return cmd
    
    async def get_audio_duration(self, file_path: str) -> Optional[float]:
        """Get audio file duration"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", file_path,
                "-f", "null",
                "-"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            _, stderr = await process.communicate()
            
            # Parse duration from stderr
            output = stderr.decode()
            for line in output.split("\n"):
                if "Duration:" in line:
                    time_str = line.split("Duration:")[1].split(",")[0].strip()
                    h, m, s = time_str.split(":")
                    duration = int(h) * 3600 + int(m) * 60 + float(s)
                    return duration
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting audio duration: {e}")
            return None
    
    async def convert_audio(
        self,
        input_file: str,
        output_file: str,
        format: str = "mp3"
    ) -> bool:
        """Convert audio file format"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-ar", str(config.SAMPLE_RATE),
                "-ac", str(config.CHANNELS),
                "-codec:a", "libmp3lame" if format == "mp3" else "copy",
                "-y",  # Overwrite output
                output_file
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            
            return process.returncode == 0
            
        except Exception as e:
            self.logger.error(f"Error converting audio: {e}")
            return False
    
    def get_version(self) -> Optional[str]:
        """Get FFmpeg version"""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                first_line = result.stdout.split("\n")[0]
                return first_line
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting FFmpeg version: {e}")
            return None

# Global FFmpeg manager
ffmpeg_manager = FFmpegManager()

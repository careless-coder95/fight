"""
Constants and Default Values
"""

# Bot Info
BOT_NAME = "VC Relay & Audio Booster"
BOT_VERSION = "2.0.0"
DEVELOPER = "@YourUsername"

# Audio Processing Constants
AUDIO_FORMATS = ["mp3", "wav", "ogg", "flac", "m4a"]
VIDEO_FORMATS = ["mp4", "mkv", "webm", "avi"]

# FFmpeg Constants
FFMPEG_TIMEOUT = 30
FFMPEG_RECONNECT_ATTEMPTS = 3

# Stream Constants
STREAM_CHUNK_SIZE = 4096
MAX_STREAM_DURATION = 3600 * 24  # 24 hours
MIN_STREAM_DURATION = 1

# Voice Chat Constants
VC_JOIN_TIMEOUT = 30
VC_RECONNECT_DELAY = 5
MAX_VC_RECONNECT_ATTEMPTS = 5

# Recording Constants
MAX_RECORDING_DURATION = 3600 * 3  # 3 hours
RECORDING_FILENAME_FORMAT = "recording_%Y%m%d_%H%M%S"

# Volume Constants
MIN_VOLUME = 0
MAX_VOLUME_LIMIT = 25
DEFAULT_VOLUME_VALUE = 10

# Bass Reduction Constants
MIN_BASS = 0
MAX_BASS = 15
DEFAULT_BASS_VALUE = 5

# Screenshare Constants
MIN_SCREEN_WIDTH = 640
MAX_SCREEN_WIDTH = 1920
MIN_SCREEN_HEIGHT = 480
MAX_SCREEN_HEIGHT = 1080
MIN_FPS = 15
MAX_FPS = 60

# Speedtest Constants
SPEEDTEST_TIMEOUT = 60

# Cache Constants
CACHE_TTL = 3600
MAX_CACHE_SIZE = 1000

# Error Messages
ERROR_NO_VC = "❌ No active voice chat found!"
ERROR_NOT_IN_VC = "❌ Assistant is not in voice chat!"
ERROR_ALREADY_IN_VC = "⚠️ Already connected to voice chat!"
ERROR_PERMISSION_DENIED = "❌ You don't have permission to use this command!"
ERROR_INVALID_CHAT = "❌ This command can only be used in groups/channels!"
ERROR_FFMPEG_NOT_FOUND = "❌ FFmpeg not found! Please install FFmpeg."

# Success Messages
SUCCESS_JOINED = "✅ Successfully joined voice chat!"
SUCCESS_LEFT = "✅ Successfully left voice chat!"
SUCCESS_STARTED = "✅ Started successfully!"
SUCCESS_STOPPED = "✅ Stopped successfully!"

# Info Messages
INFO_PROCESSING = "⏳ Processing..."
INFO_LOADING = "⏳ Loading..."
INFO_CONNECTING = "🔄 Connecting..."

# Emojis
EMOJI_MICROPHONE = "🎤"
EMOJI_SPEAKER = "🔊"
EMOJI_RECORD = "⏺"
EMOJI_PLAY = "▶️"
EMOJI_PAUSE = "⏸"
EMOJI_STOP = "⏹"
EMOJI_VOLUME = "🔊"
EMOJI_BASS = "🎵"
EMOJI_SETTINGS = "⚙️"
EMOJI_INFO = "ℹ️"
EMOJI_WARNING = "⚠️"
EMOJI_ERROR = "❌"
EMOJI_SUCCESS = "✅"
EMOJI_LOADING = "⏳"
EMOJI_FIRE = "🔥"
EMOJI_ROCKET = "🚀"
EMOJI_CHART = "📊"
EMOJI_SCREEN = "🖥"

# Command Descriptions
COMMAND_HELP = {
    "start": "Start the bot",
    "help": "Show help menu",
    "join": "Join voice chat",
    "leave": "Leave voice chat",
    "leaveall": "Leave all voice chats",
    "level": "Set volume level (1-25)",
    "bass": "Set bass reduction (0-15)",
    "mute": "Mute playback",
    "unmute": "Unmute playback",
    "startrecord": "Start recording",
    "stoprecord": "Stop recording",
    "screenshare": "Start screenshare",
    "screenshareoff": "Stop screenshare",
    "speedtest": "Run internet speed test",
    "ping": "Check bot latency",
    "stats": "Show system statistics",
    "settings": "Configure bot settings",
}

# Inline Button Text
BTN_HELP = "📚 Help"
BTN_SETTINGS = "⚙️ Settings"
BTN_STATS = "📊 Stats"
BTN_CLOSE = "❌ Close"
BTN_BACK = "◀️ Back"
BTN_JOIN_VC = "🎤 Join VC"
BTN_LEAVE_VC = "🚪 Leave VC"
BTN_VOLUME_UP = "🔊 Volume +"
BTN_VOLUME_DOWN = "🔉 Volume -"
BTN_MUTE = "🔇 Mute"
BTN_UNMUTE = "🔊 Unmute"

# Database Collections
COLLECTION_CHATS = "chats"
COLLECTION_SETTINGS = "settings"
COLLECTION_STATS = "stats"
COLLECTION_RECORDINGS = "recordings"

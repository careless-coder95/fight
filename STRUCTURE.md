# 📁 Project Structure

Complete directory structure and file organization of Telegram VC Relay Bot.

---

## 🌳 Directory Tree

```
telegram-vc-relay/
│
├── bot.py                      # Main entry point
├── generate_session.py         # String session generator
├── deploy.sh                   # Automated deployment script
├── requirements.txt            # Python dependencies
├── .env.sample                 # Environment variables template
├── .env                        # Your configuration (gitignored)
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Docker container definition
├── docker-compose.yml          # Docker compose configuration
├── LICENSE                     # MIT License
├── README.md                   # Main documentation
├── INSTALLATION.md             # Installation guide
├── TROUBLESHOOTING.md          # Troubleshooting guide
├── CHANGELOG.md                # Version history
├── STRUCTURE.md                # This file
│
├── config/                     # Configuration module
│   ├── __init__.py
│   ├── settings.py             # Settings loader
│   ├── logger.py               # Logging configuration
│   └── constants.py            # Constants and defaults
│
├── core/                       # Core functionality
│   ├── __init__.py
│   ├── client.py               # Pyrogram client manager
│   ├── vc_manager.py           # Voice chat operations
│   ├── stream_engine.py        # Audio streaming engine
│   ├── recorder.py             # Recording functionality
│   ├── player.py               # Audio playback (placeholder)
│   ├── screenshare.py          # Screenshare (placeholder)
│   ├── filters.py              # Audio filters (placeholder)
│   ├── relay.py                # Relay system (placeholder)
│   └── reconnect.py            # Auto-reconnect (placeholder)
│
├── modules/                    # Command modules
│   ├── __init__.py             # Module loader
│   ├── admin.py                # Audio control commands
│   ├── voice.py                # VC join/leave commands
│   ├── record.py               # Recording commands
│   ├── screenshare.py          # Screenshare commands
│   ├── tools.py                # Utility commands
│   ├── settings.py             # Settings commands
│   └── help.py                 # Help and documentation
│
├── database/                   # Database layer
│   ├── __init__.py
│   ├── mongodb.py              # MongoDB connection and operations
│   ├── models.py               # Data models and schemas
│   └── cache.py                # In-memory caching
│
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── ffmpeg.py               # FFmpeg utilities
│   ├── helpers.py              # Helper functions
│   ├── decorators.py           # Command decorators
│   ├── speedtest.py            # Speed test (placeholder)
│   ├── queues.py               # Queue management (placeholder)
│   ├── audio.py                # Audio utilities (placeholder)
│   └── system.py               # System utilities (placeholder)
│
├── services/                   # Background services
│   ├── relay_service.py        # Relay service (placeholder)
│   ├── stream_service.py       # Stream service (placeholder)
│   └── monitoring.py           # Monitoring service (placeholder)
│
├── assets/                     # Static assets
│   ├── thumbnails/             # Thumbnail images
│   │   └── .gitkeep
│   └── fonts/                  # Font files
│       └── .gitkeep
│
├── logs/                       # Log files (gitignored)
│   ├── .gitkeep
│   ├── bot.log                 # Main log
│   ├── error.log               # Error log
│   ├── stream.log              # Stream log
│   └── ffmpeg.log              # FFmpeg log
│
└── recordings/                 # Recorded files (gitignored)
    └── recording_*.mp3         # Recordings with timestamps
```

---

## 📄 File Descriptions

### Root Files

**bot.py**
- Main entry point
- Initializes all components
- Loads modules
- Starts event loop

**generate_session.py**
- Interactive string session generator
- Handles Pyrogram session creation
- Supports multiple sessions

**deploy.sh**
- Automated deployment script
- Installs dependencies
- Configures system
- Creates systemd service

**requirements.txt**
- Python dependencies
- Pinned versions for Python 3.10.19
- Includes all necessary packages

### Configuration (config/)

**settings.py**
- Loads environment variables
- Validates configuration
- Provides config object

**logger.py**
- Colorful console logging
- Rotating file logs
- Separate loggers for components

**constants.py**
- Bot constants
- Default values
- Error/success messages
- Command descriptions

### Core (core/)

**client.py**
- Manages Pyrogram clients
- Bot client
- Assistant clients (1 or 2)
- Client lifecycle management

**vc_manager.py**
- Voice chat operations
- Join/leave functionality
- Connection management
- Auto-reconnect logic

**stream_engine.py**
- Realtime audio streaming
- FFmpeg process management
- Stream statistics
- Volume/bass control

**recorder.py**
- Voice chat recording
- File management
- Recording metadata
- Upload to Telegram

### Modules (modules/)

**admin.py**
- `/level` - Volume control
- `/bass` - Bass reduction
- `/mute` - Mute playback
- `/unmute` - Unmute playback

**voice.py**
- `/join` - Join voice chat
- `/leave` - Leave voice chat
- `/leaveall` - Leave all chats

**record.py**
- `/startrecord` - Start recording
- `/stoprecord` - Stop recording

**screenshare.py**
- `/screenshare` - Start screenshare
- `/screenshareoff` - Stop screenshare

**tools.py**
- `/ping` - Check latency
- `/speedtest` - Speed test
- `/stats` - Statistics
- `/status` - Chat status

**settings.py**
- `/settings` - Configure bot
- Interactive settings menu
- Per-chat configuration

**help.py**
- `/start` - Start bot
- `/help` - Help menu
- Interactive documentation

### Database (database/)

**mongodb.py**
- MongoDB connection
- CRUD operations
- Chat management
- Settings storage
- Statistics tracking

**models.py**
- ChatSession model
- StreamConfig model
- RecordingData model
- StreamStats model

**cache.py**
- In-memory cache
- TTL support
- Automatic cleanup
- Fast data access

### Utils (utils/)

**ffmpeg.py**
- FFmpeg command builder
- Audio relay commands
- Recording commands
- Screenshare commands
- Audio conversion

**helpers.py**
- Readable time formatting
- Readable size formatting
- System statistics
- Admin checks
- Volume/bass formatting

**decorators.py**
- `@admin_only` - Admin check
- `@group_only` - Group check
- `@require_voice_chat` - VC check
- `@error_handler` - Error handling
- `@typing_action` - Typing indicator
- `@rate_limit` - Rate limiting
- `@log_command` - Command logging

---

## 🔄 Data Flow

### Voice Chat Join Flow
```
User sends /join
    ↓
modules/voice.py (handler)
    ↓
core/vc_manager.py (join logic)
    ↓
core/client.py (assistant client)
    ↓
Telegram Voice Chat
```

### Audio Relay Flow
```
Telegram VC Audio Input
    ↓
Assistant 1 (Recorder)
    ↓
core/stream_engine.py
    ↓
utils/ffmpeg.py (processing)
    ↓
FFmpeg Filters (volume, bass, etc.)
    ↓
Processed Audio
    ↓
Assistant 2 (Player)
    ↓
Telegram VC Audio Output
```

### Command Processing Flow
```
User Message
    ↓
Pyrogram Handler
    ↓
Decorator Chain (@admin_only, @group_only, etc.)
    ↓
Module Handler (modules/*.py)
    ↓
Core Logic (core/*.py)
    ↓
Database Update (database/*.py)
    ↓
Response to User
```

---

## 🗃️ Database Schema

### chats Collection
```javascript
{
  chat_id: Number,
  chat_title: String,
  is_active: Boolean,
  joined_at: Date,
  assistant_id: Number,
  assistant2_id: Number
}
```

### settings Collection
```javascript
{
  chat_id: Number,
  volume: Number,           // 1-25
  bass_reduction: Number,   // 0-15
  auto_gain: Boolean,
  noise_reduction: Boolean,
  is_muted: Boolean
}
```

### recordings Collection
```javascript
{
  chat_id: Number,
  filename: String,
  duration: Number,
  file_size: Number,
  format: String,
  timestamp: Date,
  file_id: String
}
```

### stats Collection
```javascript
{
  type: String,
  count: Number
}
```

---

## 🔌 Extension Points

Want to add new features? Here's where to start:

### Adding a New Command
1. Create handler in `modules/yourmodule.py`
2. Import in `modules/__init__.py`
3. Add command description to `config/constants.py`

### Adding Audio Effect
1. Add FFmpeg filter in `utils/ffmpeg.py`
2. Add control in `core/stream_engine.py`
3. Add command in `modules/admin.py`

### Adding Database Model
1. Create model in `database/models.py`
2. Add operations in `database/mongodb.py`
3. Use in your module

### Adding Background Service
1. Create service in `services/yourservice.py`
2. Start in `bot.py` main function
3. Use asyncio.create_task()

---

## 📦 Dependencies

### Python Packages
- **pyrogram**: Telegram MTProto API
- **TgCrypto**: Cryptography for Pyrogram
- **py-tgcalls**: Voice chat support
- **ntgcalls**: Native voice calls
- **motor**: Async MongoDB driver
- **pymongo**: MongoDB driver
- **uvloop**: Fast event loop
- **aiofiles**: Async file operations
- **aiohttp**: Async HTTP client
- **colorlog**: Colored logging
- **psutil**: System monitoring
- **speedtest-cli**: Speed testing

### System Dependencies
- **Python 3.10.19**: Runtime
- **FFmpeg 6.0+**: Audio processing
- **MongoDB 6.0**: Database
- **Git**: Version control

---

## 🔒 Security Notes

### Sensitive Files (.gitignored)
- `.env` - Contains secrets
- `*.session` - Pyrogram sessions
- `logs/` - May contain sensitive data
- `recordings/` - User recordings

### Best Practices
- Never commit .env file
- Regenerate sessions regularly
- Use environment variables
- Restrict sudo users
- Monitor logs for abuse

---

## 📚 Related Documentation

- [README.md](README.md) - Overview and features
- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving
- [CHANGELOG.md](CHANGELOG.md) - Version history

---

**Need help?** Contact @YourUsername on Telegram

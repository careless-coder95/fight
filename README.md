# 🎤 Telegram Realtime Voice Relay & Audio Booster Bot

> **Advanced Voice Chat Processing Engine**  
> Realtime audio relay system with live processing, volume boosting, bass reduction, recording, and screenshare capabilities.

[![Python](https://img.shields.io/badge/Python-3.10.19-blue.svg)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-green.svg)](https://pyrogram.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Features

### Core Features
- ✅ **Realtime Voice Chat Relay** - Capture and rebroadcast live VC audio instantly
- ✅ **Volume Booster** - Amplify audio up to 25 levels with anti-clipping
- ✅ **Bass Reduction** - Improve voice clarity by reducing muddy bass
- ✅ **Voice Recording** - Record VC sessions with auto-upload to Telegram
- ✅ **Screenshare** - Stream screen to voice chat (Linux VPS compatible)
- ✅ **Dual Assistant System** - Separate recording and playback accounts
- ✅ **Auto Recovery** - Automatic reconnection on failures

### Audio Processing
- 🎵 Realtime FFmpeg filtering
- 🎵 Automatic gain control (AGC)
- 🎵 Smart limiter (prevent clipping)
- 🎵 Loudness normalization
- 🎵 Optional noise reduction
- 🎵 Low latency streaming (<500ms)

### Advanced Features
- 🚀 uvloop for high performance
- 🚀 Async processing everywhere
- 🚀 MongoDB for data persistence
- 🚀 In-memory caching layer
- 🚀 Comprehensive error handling
- 🚀 Colorful logging system
- 🚀 Modern Telegram UI with inline buttons

---

## 📋 Requirements

### System Requirements
- **OS**: Ubuntu 22.04 LTS (recommended)
- **Python**: 3.10.19
- **RAM**: Minimum 1GB, Recommended 2GB+
- **CPU**: 2 cores or more
- **Storage**: 10GB+ free space

### Software Requirements
- Python 3.10.19
- FFmpeg 6.0+
- MongoDB 4.4+
- Git

---

## 🚀 Installation

### Step 1: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10.19
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.10 python3.10-dev python3.10-venv -y

# Install FFmpeg
sudo apt install ffmpeg -y

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod

# Install additional dependencies
sudo apt install -y git tmux screen
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/telegram-vc-relay.git
cd telegram-vc-relay
```

### Step 3: Create Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### Step 4: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Step 1: Get Telegram API Credentials

1. Go to [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Login with your phone number
3. Create a new application
4. Note down `API_ID` and `API_HASH`

### Step 2: Create Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the `BOT_TOKEN`

### Step 3: Generate String Sessions

**IMPORTANT**: You need Telegram USER account string sessions (not bot tokens) for voice chat functionality!

```bash
python generate_session.py
```

Follow the prompts:
1. Enter your `API_ID` and `API_HASH`
2. Enter phone number in international format (+1234567890)
3. Enter OTP code received on Telegram
4. Enter 2FA password (if enabled)
5. Copy the generated string session

**For Dual Assistant Setup**: Run the script again to generate a second session.

### Step 4: Configure Environment

```bash
cp .env.sample .env
nano .env
```

Fill in your credentials:

```env
# Telegram API Credentials
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# Assistant String Sessions
STRING_SESSION=paste_generated_session_here
STRING_SESSION2=optional_second_session_for_dual_mode

# MongoDB
MONGO_URL=mongodb://localhost:27017/
MONGO_DB_NAME=telegram_vc_relay

# Admin
LOG_GROUP_ID=-1001234567890
SUDO_USERS=123456789,987654321

# Bot Configuration
BOT_USERNAME=your_bot_username
DEFAULT_VOLUME=10
MAX_VOLUME=25
DEFAULT_BASS_REDUCTION=5
```

---

## 🎮 Running the Bot

### Method 1: Direct Run

```bash
python bot.py
```

### Method 2: Using tmux (Recommended)

```bash
tmux new -s vcrelay
python bot.py

# Detach: Press Ctrl+B then D
# Reattach: tmux attach -t vcrelay
```

### Method 3: Using screen

```bash
screen -S vcrelay
python bot.py

# Detach: Press Ctrl+A then D
# Reattach: screen -r vcrelay
```

### Method 4: systemd Service

Create service file:

```bash
sudo nano /etc/systemd/system/vcrelay.service
```

Add content:

```ini
[Unit]
Description=Telegram VC Relay Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/telegram-vc-relay
ExecStart=/path/to/telegram-vc-relay/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable vcrelay
sudo systemctl start vcrelay
sudo systemctl status vcrelay
```

---

## 📱 Commands

### Voice Chat Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/join` | Join voice chat | `/join` |
| `/leave` | Leave voice chat | `/leave` |
| `/leaveall` | Leave all voice chats | `/leaveall` |

### Audio Control Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/level <1-25>` | Set volume level | `/level 15` |
| `/bass <0-15>` | Set bass reduction | `/bass 8` |
| `/mute` | Mute playback | `/mute` |
| `/unmute` | Unmute playback | `/unmute` |

### Recording Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/startrecord` | Start recording VC | `/startrecord` |
| `/stoprecord` | Stop recording | `/stoprecord` |

### Screenshare Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/screenshare` | Start screenshare | `/screenshare` |
| `/screenshareoff` | Stop screenshare | `/screenshareoff` |

### Utility Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/speedtest` | Run speed test | `/speedtest` |
| `/ping` | Check latency | `/ping` |
| `/stats` | Show statistics | `/stats` |
| `/settings` | Bot settings | `/settings` |
| `/help` | Show help menu | `/help` |

---

## 🏗️ Architecture

### System Flow

```
Telegram Voice Chat
        ↓
Assistant 1 (Recorder)
        ↓
PCM Audio Capture
        ↓
FFmpeg Processing
├── Volume Boost
├── Bass Reduction
├── Auto Gain Control
├── Limiter
└── Loudness Normalization
        ↓
Processed Audio Stream
        ↓
Assistant 2 (Player)
        ↓
Telegram Voice Chat Output
```

### Dual Assistant Architecture

**Single Assistant Mode**:
- One account for both recording and playback
- Same voice chat

**Dual Assistant Mode**:
- Assistant 1: Recording/Input
- Assistant 2: Playback/Output
- Can work in same or different voice chats
- Better isolation and performance

---

## 🔧 Audio Processing Details

### Volume Boosting

- **Range**: 1-25 levels
- **Method**: FFmpeg volume filter
- **Anti-clipping**: Smart limiter
- **Realtime**: No restart needed

### Bass Reduction

- **Range**: 0-15 levels
- **Method**: Highpass filter
- **Frequency**: 80Hz - 230Hz cutoff
- **Purpose**: Improve voice clarity

### Auto Gain Control (AGC)

- **Method**: Loudness normalization
- **Target**: -16 LUFS
- **True Peak**: -1.5 dB
- **LRA**: 11 LU

### Smart Limiter

- **Limit**: 0.9 (prevent clipping)
- **Attack**: 5ms
- **Release**: 50ms

---

## 📊 Troubleshooting

### Bot Not Starting

```bash
# Check Python version
python --version  # Should be 3.10.19

# Check dependencies
pip list

# Check FFmpeg
ffmpeg -version

# Check MongoDB
sudo systemctl status mongod

# Check logs
cat logs/bot.log
cat logs/error.log
```

### Voice Chat Issues

**Problem**: Can't join voice chat

**Solutions**:
1. Check if group has active voice chat
2. Verify assistant account has admin rights
3. Check string session validity
4. Regenerate string session if expired

**Problem**: Audio not playing

**Solutions**:
1. Check volume level: `/level 15`
2. Verify not muted: `/unmute`
3. Check FFmpeg logs: `cat logs/ffmpeg.log`
4. Restart bot

**Problem**: High latency

**Solutions**:
1. Reduce buffer size in settings
2. Check network speed: `/speedtest`
3. Use closer VPS region
4. Enable uvloop in .env

### Recording Issues

**Problem**: Recording not saving

**Solutions**:
1. Check disk space: `df -h`
2. Verify write permissions
3. Check FFmpeg: `ffmpeg -version`

### String Session Issues

**Problem**: AuthKeyUnregistered error

**Solutions**:
1. Regenerate string session
2. Verify API_ID and API_HASH
3. Check if account was logged out
4. Use: `python generate_session.py`

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker

```bash
# Build image
docker build -t vcrelay .

# Run container
docker run -d --name vcrelay \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  vcrelay
```

---

## 📈 Performance Optimization

### For Low-End VPS (1GB RAM)

```env
STREAM_BUFFER_SIZE=32768
ENABLE_UVLOOP=true
ENABLE_NOISE_REDUCTION=false
```

### For High-End VPS (4GB+ RAM)

```env
STREAM_BUFFER_SIZE=131072
ENABLE_UVLOOP=true
ENABLE_NOISE_REDUCTION=true
ENABLE_AUTO_GAIN=true
```

### Network Optimization

```bash
# Increase file descriptors
ulimit -n 65536

# Optimize TCP
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.wmem_max=134217728
```

---

## 🔐 Security

### Best Practices

1. **Keep string sessions private** - Never share or commit to git
2. **Use environment variables** - Don't hardcode credentials
3. **Restrict sudo users** - Only trusted admins
4. **Regular updates** - Keep dependencies updated
5. **Monitor logs** - Check for suspicious activity

### Recommended .gitignore

```
.env
*.session
*.session-journal
logs/
__pycache__/
venv/
*.pyc
```

---

## 📝 Changelog

### Version 2.0.0 (Latest)
- ✅ Complete rewrite for Python 3.10.19
- ✅ Realtime audio relay system
- ✅ Dual assistant architecture
- ✅ Advanced FFmpeg processing
- ✅ MongoDB integration
- ✅ Screenshare support
- ✅ Auto recovery system
- ✅ Modern UI with inline buttons

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/telegram-vc-relay/issues)
- **Telegram**: [@YourUsername](https://t.me/yourusername)
- **Documentation**: [Wiki](https://github.com/yourusername/telegram-vc-relay/wiki)

---

## 🙏 Credits

- [Pyrogram](https://pyrogram.org) - Telegram MTProto API framework
- [PyTgCalls](https://github.com/pytgcalls/pytgcalls) - Voice chat library
- [FFmpeg](https://ffmpeg.org) - Audio/video processing
- [MongoDB](https://mongodb.com) - Database

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ for the Telegram community**

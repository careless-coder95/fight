# 📦 Installation Guide

Complete step-by-step installation guide for Telegram VC Relay Bot.

---

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Ubuntu 22.04 LTS (or similar Linux distro)
- **CPU**: 2 cores
- **RAM**: 1 GB
- **Storage**: 10 GB free space
- **Network**: 10 Mbps upload/download

### Recommended Requirements
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 4+ cores
- **RAM**: 2 GB+
- **Storage**: 20 GB+ SSD
- **Network**: 50+ Mbps upload/download

---

## 🚀 Quick Installation (Ubuntu 22.04)

### Step 1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Python 3.10.19

```bash
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.10
sudo apt install -y python3.10 python3.10-dev python3.10-venv python3-pip

# Verify installation
python3.10 --version
```

### Step 3: Install FFmpeg

```bash
# Install FFmpeg 6.x
sudo apt install -y ffmpeg

# Verify installation
ffmpeg -version
```

### Step 4: Install MongoDB

```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update and install
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify installation
sudo systemctl status mongod
```

### Step 5: Install Additional Tools

```bash
sudo apt install -y git tmux screen htop curl wget
```

### Step 6: Clone Repository

```bash
cd ~
git clone https://github.com/yourusername/telegram-vc-relay.git
cd telegram-vc-relay
```

### Step 7: Setup Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 8: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Step 1: Get Telegram API Credentials

1. Visit: https://my.telegram.org/apps
2. Login with your phone number
3. Click on "API Development Tools"
4. Create a new application
5. Note your `API_ID` and `API_HASH`

### Step 2: Create Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow the instructions to create your bot
4. Copy the `BOT_TOKEN`

### Step 3: Generate String Sessions

**IMPORTANT**: You need USER account string sessions for voice chat functionality!

```bash
python generate_session.py
```

Follow the prompts:
- Enter API_ID and API_HASH
- Enter phone number (international format: +1234567890)
- Enter OTP code from Telegram
- Enter 2FA password if you have one
- Copy the generated string session

**For Dual Assistant Setup**:
Run the script again to generate a second session.

### Step 4: Setup Environment File

```bash
cp .env.sample .env
nano .env
```

Fill in your configuration:

```env
# Telegram API
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Assistant Sessions
STRING_SESSION=your_first_session_here
STRING_SESSION2=your_second_session_here  # Optional

# MongoDB
MONGO_URL=mongodb://localhost:27017/
MONGO_DB_NAME=telegram_vc_relay

# Admin
LOG_GROUP_ID=-1001234567890
SUDO_USERS=123456789,987654321

# Bot Config
BOT_USERNAME=your_bot_username
DEFAULT_VOLUME=10
MAX_VOLUME=25
```

Save and exit (Ctrl+X, then Y, then Enter).

---

## 🏃 Running the Bot

### Method 1: Direct Run

```bash
python bot.py
```

### Method 2: Using tmux (Recommended for VPS)

```bash
# Create new tmux session
tmux new -s vcrelay

# Run bot
python bot.py

# Detach from session: Ctrl+B then D
# Reattach to session:
tmux attach -t vcrelay

# List sessions:
tmux ls

# Kill session:
tmux kill-session -t vcrelay
```

### Method 3: Using screen

```bash
# Create new screen session
screen -S vcrelay

# Run bot
python bot.py

# Detach from session: Ctrl+A then D
# Reattach to session:
screen -r vcrelay

# List sessions:
screen -ls

# Kill session:
screen -X -S vcrelay quit
```

### Method 4: systemd Service (Auto-start on boot)

Create service file:

```bash
sudo nano /etc/systemd/system/vcrelay.service
```

Add content (replace paths with your actual paths):

```ini
[Unit]
Description=Telegram VC Relay Bot
After=network.target mongod.service

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/telegram-vc-relay
ExecStart=/home/your_username/telegram-vc-relay/venv/bin/python bot.py
Restart=always
RestartSec=10
StandardOutput=append:/home/your_username/telegram-vc-relay/logs/systemd.log
StandardError=append:/home/your_username/telegram-vc-relay/logs/systemd_error.log

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (auto-start on boot)
sudo systemctl enable vcrelay

# Start service
sudo systemctl start vcrelay

# Check status
sudo systemctl status vcrelay

# View logs
sudo journalctl -u vcrelay -f

# Stop service
sudo systemctl stop vcrelay

# Restart service
sudo systemctl restart vcrelay
```

---

## 🔍 Verification

### Check if Bot is Running

```bash
# Check process
ps aux | grep bot.py

# Check logs
tail -f logs/bot.log

# Check MongoDB connection
mongo --eval "db.adminCommand('ping')"
```

### Test Bot

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. You should see the welcome message

### Test Voice Chat

1. Create a group
2. Add your bot to the group
3. Make bot admin (required for VC access)
4. Start a voice chat
5. Send `/join` in the group
6. Bot should join the voice chat

---

## 🐛 Troubleshooting

### Python Version Issues

```bash
# Check Python version
python3.10 --version

# If command not found, install:
sudo apt install python3.10
```

### FFmpeg Not Found

```bash
# Install FFmpeg
sudo apt install ffmpeg

# Check installation
which ffmpeg
ffmpeg -version
```

### MongoDB Connection Failed

```bash
# Start MongoDB
sudo systemctl start mongod

# Check status
sudo systemctl status mongod

# Check logs
sudo journalctl -u mongod
```

### String Session Invalid

```bash
# Regenerate session
python generate_session.py

# Update .env file with new session
nano .env
```

### Permission Denied

```bash
# Make files executable
chmod +x bot.py generate_session.py

# Fix permissions
sudo chown -R $USER:$USER ~/telegram-vc-relay
```

### Port Already in Use

```bash
# Check what's using port 27017 (MongoDB)
sudo lsof -i :27017

# Kill process if needed
sudo kill -9 <PID>
```

---

## 📊 Monitoring

### View Logs

```bash
# Main log
tail -f logs/bot.log

# Error log
tail -f logs/error.log

# Stream log
tail -f logs/stream.log

# FFmpeg log
tail -f logs/ffmpeg.log
```

### System Resources

```bash
# CPU and Memory
htop

# Disk space
df -h

# Network usage
iftop
```

### Bot Status

```bash
# Send /stats command in Telegram
# or
# Check systemd status
sudo systemctl status vcrelay
```

---

## 🔄 Updates

### Update Bot

```bash
cd ~/telegram-vc-relay
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart vcrelay  # If using systemd
```

### Update Python Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 🗑️ Uninstallation

```bash
# Stop bot
sudo systemctl stop vcrelay
sudo systemctl disable vcrelay
sudo rm /etc/systemd/system/vcrelay.service

# Remove files
rm -rf ~/telegram-vc-relay

# Remove virtual environment
rm -rf ~/telegram-vc-relay/venv

# Optionally remove MongoDB
sudo systemctl stop mongod
sudo apt remove mongodb-org
```

---

## 📞 Support

If you encounter issues:

1. Check logs: `tail -f logs/error.log`
2. Read troubleshooting section above
3. Check GitHub Issues
4. Contact support: @YourUsername

---

**Installation Complete! 🎉**

Your bot should now be running. Send `/help` to your bot in Telegram to see available commands.

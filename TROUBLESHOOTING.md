# 🔧 Troubleshooting Guide

Common issues and their solutions for Telegram VC Relay Bot.

---

## 📋 Table of Contents

1. [Installation Issues](#installation-issues)
2. [Configuration Issues](#configuration-issues)
3. [Voice Chat Issues](#voice-chat-issues)
4. [Audio Issues](#audio-issues)
5. [Recording Issues](#recording-issues)
6. [Performance Issues](#performance-issues)
7. [Database Issues](#database-issues)
8. [Network Issues](#network-issues)
9. [Python Issues](#python-issues)
10. [General Debugging](#general-debugging)

---

## 🛠️ Installation Issues

### Python Version Mismatch

**Problem**: Wrong Python version installed

**Solution**:
```bash
# Check Python version
python3.10 --version

# If not installed
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-dev python3.10-venv
```

### FFmpeg Not Found

**Problem**: `❌ FFmpeg not found!`

**Solution**:
```bash
# Install FFmpeg
sudo apt update
sudo apt install ffmpeg -y

# Verify
ffmpeg -version
which ffmpeg
```

### Dependency Installation Fails

**Problem**: `pip install -r requirements.txt` fails

**Solution**:
```bash
# Update pip
pip install --upgrade pip setuptools wheel

# Install with verbose output
pip install -r requirements.txt -v

# If specific package fails, try individually
pip install pyrogram
pip install TgCrypto
# etc.
```

---

## ⚙️ Configuration Issues

### Invalid API Credentials

**Problem**: `❌ Invalid API_ID or API_HASH!`

**Solution**:
1. Visit https://my.telegram.org/apps
2. Login and get correct API_ID and API_HASH
3. Update .env file:
```bash
nano .env
# Update API_ID and API_HASH
```

### Invalid String Session

**Problem**: `❌ Invalid STRING_SESSION!` or `AuthKeyUnregistered`

**Solution**:
```bash
# Regenerate string session
python generate_session.py

# Copy the generated session
# Update .env file
nano .env
# Paste new STRING_SESSION
```

### Bot Token Invalid

**Problem**: Bot not starting due to invalid token

**Solution**:
1. Message @BotFather on Telegram
2. Send `/mybots`
3. Select your bot
4. Get new token if needed
5. Update .env file

### Missing Environment Variables

**Problem**: `❌ Missing required configuration`

**Solution**:
```bash
# Check .env file exists
ls -la .env

# If not, copy sample
cp .env.sample .env

# Edit and fill all required fields
nano .env
```

---

## 🎤 Voice Chat Issues

### Cannot Join Voice Chat

**Problem**: Bot cannot join voice chat

**Possible Causes & Solutions**:

1. **No active voice chat**
   - Start a voice chat in the group first
   - Then send `/join`

2. **Assistant not admin**
   - Make the assistant account admin in the group
   - Give voice chat permissions

3. **Wrong chat type**
   - Command only works in groups/supergroups
   - Not in private chats

4. **String session expired**
   ```bash
   python generate_session.py
   # Generate new session and update .env
   ```

### Assistant Disconnects Frequently

**Problem**: Assistant keeps disconnecting from VC

**Solutions**:

1. **Network issues**
   ```bash
   # Check network
   ping google.com
   
   # Run speedtest
   # In Telegram: /speedtest
   ```

2. **Enable auto-recovery**
   ```bash
   # In .env file
   ENABLE_AUTO_RECOVERY=true
   ```

3. **Increase buffer size**
   ```bash
   # In .env file
   STREAM_BUFFER_SIZE=131072
   ```

### Cannot Leave Voice Chat

**Problem**: `/leave` command not working

**Solution**:
```bash
# Force leave all chats
# In Telegram: /leaveall

# Restart bot
sudo systemctl restart vcrelay
# or
pkill -f bot.py && python bot.py
```

---

## 🔊 Audio Issues

### No Audio Playing

**Problem**: Bot connected but no audio

**Solutions**:

1. **Check if muted**
   ```
   # In Telegram: /unmute
   ```

2. **Check volume level**
   ```
   # In Telegram: /level 15
   ```

3. **Check stream status**
   ```
   # In Telegram: /status
   ```

4. **Restart stream**
   ```
   # Leave and rejoin
   /leave
   /join
   ```

### Audio Quality Poor

**Problem**: Low quality, choppy, or distorted audio

**Solutions**:

1. **Increase bitrate**
   ```bash
   # In .env file
   BITRATE=256k  # or 320k
   ```

2. **Adjust sample rate**
   ```bash
   # In .env file
   SAMPLE_RATE=48000
   ```

3. **Enable auto gain**
   ```
   # In Telegram: /settings
   # Enable Auto Gain Control
   ```

4. **Reduce bass reduction**
   ```
   # In Telegram: /bass 3
   # Lower values = less processing
   ```

### Audio Delay/Latency

**Problem**: High latency between input and output

**Solutions**:

1. **Reduce buffer size**
   ```bash
   # In .env file
   STREAM_BUFFER_SIZE=32768
   MAX_LATENCY_MS=300
   ```

2. **Enable uvloop**
   ```bash
   # In .env file
   ENABLE_UVLOOP=true
   ```

3. **Check network**
   ```
   # In Telegram: /speedtest
   # Need >10Mbps for good performance
   ```

4. **Use faster VPS**
   - Upgrade to SSD VPS
   - Choose datacenter closer to you

### Volume Too Low/High

**Problem**: Audio volume not as expected

**Solutions**:
```
# Set volume level (1-25)
/level 15

# For louder audio
/level 20

# For softer audio
/level 8
```

---

## 📹 Recording Issues

### Recording Not Saving

**Problem**: Recording stops but file not found

**Solutions**:

1. **Check disk space**
   ```bash
   df -h
   # Need at least 1GB free
   ```

2. **Check permissions**
   ```bash
   ls -la recordings/
   chmod 755 recordings/
   ```

3. **Check FFmpeg**
   ```bash
   ffmpeg -version
   # Check logs
   cat logs/ffmpeg.log
   ```

### Recording Upload Fails

**Problem**: Recording saved but upload to Telegram fails

**Solutions**:

1. **File too large**
   - Telegram limit: 2GB for bots
   - Split recording or reduce quality

2. **Network timeout**
   ```bash
   # Retry manually
   # File saved in recordings/ directory
   ```

3. **Bot token issues**
   - Verify bot token in .env
   - Regenerate if needed

### Recording Quality Poor

**Problem**: Low quality recordings

**Solutions**:
```bash
# In .env file
RECORDING_FORMAT=mp3
RECORDING_QUALITY=320  # Maximum quality
```

---

## 🚀 Performance Issues

### High CPU Usage

**Problem**: Bot using too much CPU

**Solutions**:

1. **Enable uvloop**
   ```bash
   # In .env file
   ENABLE_UVLOOP=true
   ```

2. **Disable noise reduction**
   ```bash
   # In .env file
   ENABLE_NOISE_REDUCTION=false
   ```

3. **Reduce audio processing**
   ```
   # In Telegram:
   /settings
   # Disable unnecessary features
   ```

4. **Upgrade VPS**
   - Need minimum 2 CPU cores

### High Memory Usage

**Problem**: Bot using too much RAM

**Solutions**:

1. **Reduce buffer size**
   ```bash
   # In .env file
   STREAM_BUFFER_SIZE=32768
   ```

2. **Clear cache**
   ```bash
   # Restart bot
   sudo systemctl restart vcrelay
   ```

3. **Check for memory leaks**
   ```bash
   # Monitor with htop
   htop
   ```

### Bot Crashes Frequently

**Problem**: Bot stops unexpectedly

**Solutions**:

1. **Check error logs**
   ```bash
   tail -50 logs/error.log
   ```

2. **Enable auto-restart**
   ```bash
   # Using systemd (already configured)
   sudo systemctl enable vcrelay
   ```

3. **Increase system limits**
   ```bash
   ulimit -n 65536
   ```

---

## 🗄️ Database Issues

### MongoDB Connection Failed

**Problem**: `❌ MongoDB connection failed`

**Solutions**:

1. **Start MongoDB**
   ```bash
   sudo systemctl start mongod
   sudo systemctl status mongod
   ```

2. **Check MongoDB URL**
   ```bash
   # In .env file
   MONGO_URL=mongodb://localhost:27017/
   ```

3. **Check MongoDB logs**
   ```bash
   sudo journalctl -u mongod -n 50
   ```

4. **Reinstall MongoDB**
   ```bash
   sudo apt remove mongodb-org
   sudo apt autoremove
   # Then reinstall (see INSTALLATION.md)
   ```

### Database Errors

**Problem**: Database read/write errors

**Solutions**:

1. **Check disk space**
   ```bash
   df -h
   ```

2. **Repair MongoDB**
   ```bash
   sudo systemctl stop mongod
   sudo mongod --repair
   sudo systemctl start mongod
   ```

3. **Clear database**
   ```bash
   mongo
   > use telegram_vc_relay
   > db.dropDatabase()
   > exit
   ```

---

## 🌐 Network Issues

### Flood Wait Errors

**Problem**: `FloodWait: must wait X seconds`

**Solution**:
- Bot will auto-wait and retry
- This is Telegram's rate limiting
- Be patient, it will continue automatically

### Connection Timeout

**Problem**: Network timeouts, connection refused

**Solutions**:

1. **Check internet**
   ```bash
   ping 8.8.8.8
   curl https://api.telegram.org
   ```

2. **Check firewall**
   ```bash
   sudo ufw status
   # Allow if needed
   sudo ufw allow 443
   ```

3. **Use VPN/Proxy**
   - If Telegram blocked in your region
   - Configure proxy in Pyrogram

### Slow Performance

**Problem**: Commands slow to respond

**Solutions**:

1. **Check network speed**
   ```
   # In Telegram: /speedtest
   # Need >5Mbps minimum
   ```

2. **Choose better VPS location**
   - Closer to Telegram servers
   - European or Asian datacenters usually best

---

## 🐍 Python Issues

### Import Errors

**Problem**: `ModuleNotFoundError` or `ImportError`

**Solutions**:

1. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

2. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check Python version**
   ```bash
   python --version
   # Should be 3.10.x
   ```

### Syntax Errors

**Problem**: Code syntax errors

**Solution**:
```bash
# Verify Python 3.10 is being used
which python
python --version

# Not Python 3.12+ which has different syntax
```

---

## 🔍 General Debugging

### Enable Debug Logging

```bash
# In .env file
LOG_LEVEL=DEBUG

# Restart bot
sudo systemctl restart vcrelay
```

### Check All Logs

```bash
# Main log
tail -f logs/bot.log

# Error log
tail -f logs/error.log

# Stream log
tail -f logs/stream.log

# FFmpeg log
tail -f logs/ffmpeg.log

# Systemd log (if using systemd)
sudo journalctl -u vcrelay -f
```

### Test Individual Components

```bash
# Test Python
python --version

# Test FFmpeg
ffmpeg -version

# Test MongoDB
mongo --eval "db.adminCommand('ping')"

# Test bot token
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"
```

### Reset Everything

```bash
# Stop bot
sudo systemctl stop vcrelay

# Clear logs
rm logs/*.log

# Clear database
mongo telegram_vc_relay --eval "db.dropDatabase()"

# Restart MongoDB
sudo systemctl restart mongod

# Start bot
sudo systemctl start vcrelay
```

---

## 📞 Getting Help

If none of these solutions work:

1. **Check logs thoroughly**
   ```bash
   cat logs/error.log | grep -i error
   ```

2. **Create GitHub Issue**
   - Include error logs
   - Include your .env config (hide sensitive data!)
   - Describe steps to reproduce

3. **Join Support Chat**
   - Telegram: @YourSupportGroup

4. **Read Documentation**
   - README.md
   - INSTALLATION.md

---

## 🎯 Quick Diagnostic Checklist

Use this checklist to diagnose issues:

- [ ] Python 3.10.19 installed? `python3.10 --version`
- [ ] FFmpeg installed? `ffmpeg -version`
- [ ] MongoDB running? `sudo systemctl status mongod`
- [ ] Virtual environment activated? `which python`
- [ ] Dependencies installed? `pip list`
- [ ] .env file exists and filled? `cat .env`
- [ ] String session valid? Try regenerating
- [ ] Bot token valid? Test with curl
- [ ] Network working? `ping google.com`
- [ ] Disk space available? `df -h`
- [ ] Logs checked? `tail logs/error.log`

If all above check out and still having issues, contact support!

---

**Remember**: Most issues are configuration related. Double-check your .env file! 🔍

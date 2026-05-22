# ⚡ Quick Start Guide

Get up and running in 5 minutes!

---

## 🎯 Prerequisites

- Ubuntu 22.04 VPS
- Root/sudo access
- Telegram account
- 30 minutes of time

---

## 🚀 Installation (5 Steps)

### 1️⃣ Clone Repository

```bash
cd ~
git clone https://github.com/yourusername/telegram-vc-relay.git
cd telegram-vc-relay
```

### 2️⃣ Run Deployment Script

```bash
chmod +x deploy.sh
./deploy.sh
```

This will install:
- Python 3.10
- FFmpeg
- MongoDB
- All dependencies

### 3️⃣ Generate String Session

```bash
python generate_session.py
```

Follow prompts:
- Enter API_ID and API_HASH (from https://my.telegram.org/apps)
- Enter phone number (+1234567890)
- Enter OTP code
- Copy the session string

### 4️⃣ Configure Environment

```bash
nano .env
```

Fill in:
```env
API_ID=12345678
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
STRING_SESSION=your_session_string
MONGO_URL=mongodb://localhost:27017/
LOG_GROUP_ID=-1001234567890
SUDO_USERS=123456789
```

Save: `Ctrl+X` → `Y` → `Enter`

### 5️⃣ Start Bot

**Option A: Direct Run**
```bash
python bot.py
```

**Option B: systemd (Recommended)**
```bash
sudo systemctl start vcrelay
sudo systemctl status vcrelay
```

---

## ✅ Verification

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. You should see the welcome message! 🎉

---

## 🎤 First Voice Chat

1. Create a group
2. Add your bot
3. Make bot admin
4. Start voice chat
5. Send `/join`
6. Send `/level 15`
7. Bot is now relaying audio!

---

## 📋 Quick Commands

```
/join       - Join voice chat
/leave      - Leave voice chat
/level 15   - Set volume to 15
/bass 5     - Set bass reduction to 5
/mute       - Mute playback
/unmute     - Unmute playback
/stats      - Show statistics
/help       - Full help menu
```

---

## 🔧 Quick Troubleshooting

**Bot not starting?**
```bash
cat logs/error.log
```

**Can't join VC?**
- Check if VC is active
- Make assistant admin
- Check string session

**No audio?**
```
/level 15
/unmute
```

**Need help?**
- Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Check [INSTALLATION.md](INSTALLATION.md)
- Contact @YourUsername

---

## 🎓 Next Steps

1. ✅ **Configure Settings**
   - Send `/settings` in your group
   - Adjust volume, bass, etc.

2. ✅ **Try Recording**
   - `/startrecord` - Start
   - `/stoprecord` - Stop and get file

3. ✅ **Monitor Performance**
   - `/stats` - System stats
   - `/ping` - Check latency
   - `/speedtest` - Network speed

4. ✅ **Read Full Docs**
   - [README.md](README.md) - Complete guide
   - [STRUCTURE.md](STRUCTURE.md) - Project structure

---

## 💡 Pro Tips

1. **Use tmux for VPS**
   ```bash
   tmux new -s vcrelay
   python bot.py
   # Ctrl+B then D to detach
   ```

2. **Enable systemd for auto-restart**
   ```bash
   sudo systemctl enable vcrelay
   ```

3. **Monitor logs**
   ```bash
   tail -f logs/bot.log
   ```

4. **Backup your .env**
   ```bash
   cp .env .env.backup
   ```

---

## ⚠️ Important Notes

- **String Session**: Keep it secret! It's like a password.
- **Admin Rights**: Assistant needs admin in groups.
- **MongoDB**: Must be running for bot to work.
- **Network**: Need good internet (>10 Mbps).

---

**That's it! You're ready to go! 🚀**

Any issues? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

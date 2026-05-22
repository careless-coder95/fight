#!/bin/bash

# Telegram VC Relay Bot - Deployment Script
# This script helps deploy the bot on a VPS

set -e

echo "=========================================="
echo "Telegram VC Relay Bot - Deployment Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}❌ Please do not run this script as root!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Running as non-root user${NC}"

# Check OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo -e "${RED}❌ Cannot determine OS${NC}"
    exit 1
fi

echo -e "${GREEN}✓ OS: $OS $VER${NC}"

# Check if Ubuntu 22.04
if [[ "$OS" != *"Ubuntu"* ]] || [[ "$VER" != "22.04" ]]; then
    echo -e "${YELLOW}⚠️  Warning: This script is optimized for Ubuntu 22.04${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install system dependencies
echo ""
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y software-properties-common wget curl git build-essential

# Install Python 3.10
echo ""
echo "🐍 Installing Python 3.10..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-dev python3.10-venv python3-pip

# Verify Python
PYTHON_VERSION=$(python3.10 --version 2>&1)
echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"

# Install FFmpeg
echo ""
echo "🎬 Installing FFmpeg..."
sudo apt install -y ffmpeg
FFMPEG_VERSION=$(ffmpeg -version | head -n 1)
echo -e "${GREEN}✓ $FFMPEG_VERSION${NC}"

# Install MongoDB
echo ""
echo "🗄️  Installing MongoDB..."
if ! command -v mongod &> /dev/null; then
    wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
    sudo apt update
    sudo apt install -y mongodb-org
    sudo systemctl start mongod
    sudo systemctl enable mongod
fi

MONGO_STATUS=$(sudo systemctl is-active mongod)
if [ "$MONGO_STATUS" = "active" ]; then
    echo -e "${GREEN}✓ MongoDB is running${NC}"
else
    echo -e "${RED}❌ MongoDB is not running${NC}"
    exit 1
fi

# Install additional tools
echo ""
echo "🔧 Installing additional tools..."
sudo apt install -y tmux screen htop

# Setup project
echo ""
echo "📁 Setting up project..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.10 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Copying .env.sample to .env..."
    cp .env.sample .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit .env file with your credentials!${NC}"
    echo "Run: nano .env"
    echo ""
fi

# Make scripts executable
chmod +x bot.py generate_session.py

# Create systemd service
echo ""
read -p "Do you want to create systemd service? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SERVICE_FILE="/etc/systemd/system/vcrelay.service"
    
    sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Telegram VC Relay Bot
After=network.target mongod.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python bot.py
Restart=always
RestartSec=10
StandardOutput=append:$(pwd)/logs/systemd.log
StandardError=append:$(pwd)/logs/systemd_error.log

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable vcrelay
    
    echo -e "${GREEN}✓ Systemd service created${NC}"
    echo "Start with: sudo systemctl start vcrelay"
    echo "Check status: sudo systemctl status vcrelay"
fi

# Summary
echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Generate string session: python generate_session.py"
echo "2. Edit .env file: nano .env"
echo "3. Run bot: python bot.py"
echo "   OR use systemd: sudo systemctl start vcrelay"
echo ""
echo "For more help, see:"
echo "- README.md"
echo "- INSTALLATION.md"
echo ""
echo "Enjoy! 🎉"

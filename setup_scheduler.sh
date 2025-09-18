#!/bin/bash

# Setup script for Twitter Agent Scheduler

echo "🔧 Setting up Twitter Agent Scheduler..."

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Please run this script from the twitter-agent directory"
    exit 1
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please create it first with:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Make scheduler.py executable
chmod +x scheduler.py
echo "✅ Made scheduler.py executable"

# Copy service file to systemd directory
echo "📋 Installing systemd service..."
sudo cp twitter-agent-scheduler.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start the service
echo "🚀 Starting Twitter Agent Scheduler service..."
sudo systemctl enable twitter-agent-scheduler.service
sudo systemctl start twitter-agent-scheduler.service

# Check service status
echo "🔍 Checking service status..."
sudo systemctl status twitter-agent-scheduler.service --no-pager

echo "✅ Setup complete!"
echo "📝 To check logs: sudo journalctl -u twitter-agent-scheduler.service -f"
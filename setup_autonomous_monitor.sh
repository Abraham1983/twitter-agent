#!/bin/bash
# Setup script for AutonomIQ Twitter Agent Autonomous Monitor service

echo "Setting up AutonomIQ Twitter Agent Autonomous Monitor service..."

# Copy service file to systemd directory
sudo cp autonomiq-autonomous-monitor.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable autonomiq-autonomous-monitor.service

# Start the service
sudo systemctl start autonomiq-autonomous-monitor.service

echo "AutonomIQ Twitter Agent Autonomous Monitor service installed and started!"
echo ""
echo "To check the status of the service, run:"
echo "  sudo systemctl status autonomiq-autonomous-monitor.service"
echo ""
echo "To view the logs, run:"
echo "  journalctl -u autonomiq-autonomous-monitor.service -f"
# Twitter Agent Scheduler Setup Instructions

## Prerequisites
- Make sure you're in the twitter-agent directory
- Ensure your virtual environment is set up with all dependencies installed

## Setup Steps

1. Make the scheduler script executable:
   ```bash
   chmod +x scheduler.py
   ```

2. Make the setup script executable:
   ```bash
   chmod +x setup_scheduler.sh
   ```

3. Run the setup script with sudo:
   ```bash
   sudo ./setup_scheduler.sh
   ```

## Manual Service Setup (if needed)

If you prefer to set up the service manually:

1. Copy the service file:
   ```bash
   sudo cp twitter-agent-scheduler.service /etc/systemd/system/
   ```

2. Reload systemd:
   ```bash
   sudo systemctl daemon-reload
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl enable twitter-agent-scheduler.service
   sudo systemctl start twitter-agent-scheduler.service
   ```

4. Check the service status:
   ```bash
   sudo systemctl status twitter-agent-scheduler.service
   ```

## Testing the Scheduler

To test the scheduler without waiting for the scheduled time:

1. Run the scheduler manually:
   ```bash
   cd /home/simai/twitter-agent
   source venv/bin/activate
   python scheduler.py
   ```

2. Or run the main script directly:
   ```bash
   cd /home/simai/twitter-agent
   source venv/bin/activate
   python main.py
   ```

## Monitoring

To monitor the service logs:
```bash
sudo journalctl -u twitter-agent-scheduler.service -f
```

The scheduler is configured to post twice daily:
- 9:00 AM (morning post)
- 3:00 PM (afternoon post)
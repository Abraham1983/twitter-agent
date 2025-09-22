#!/bin/bash
# Setup script for AutonomIQ Twitter automation cron jobs

echo "Setting up AutonomIQ Twitter automation cron jobs..."

# Create cron jobs for daily posting
(crontab -l 2>/dev/null; echo "0 9 * * * cd /home/simai/twitter-agent && /home/simai/twitter-agent/venv/bin/python daily_tweet_generator.py >> /home/simai/twitter-agent/system_output.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "0 15 * * * cd /home/simai/twitter-agent && /home/simai/twitter-agent/venv/bin/python daily_tweet_generator.py >> /home/simai/twitter-agent/system_output.log 2>&1") | crontab -

echo "Cron jobs installed:"
echo "  9:00 AM - Morning Twitter post"
echo "  3:00 PM - Afternoon Twitter post"

echo ""
echo "To update your daily focus, run:"
echo "  ./update_daily_reminder.py"
echo ""
echo "To manually generate content, run:"
echo "  ./daily_tweet_generator.py"
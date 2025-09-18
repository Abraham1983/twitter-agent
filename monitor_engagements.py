#!/usr/bin/env python3
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.monitoring_agent import MonitoringAgent

def main():
    """Main monitoring function"""
    print("🚀 Starting Twitter Engagement Monitor")
    print("=" * 50)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize the monitoring agent
    monitor = MonitoringAgent()
    
    # Run continuous monitoring
    monitor.monitor_new_engagements(interval_minutes=5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Monitor error: {e}")
        sys.exit(1)
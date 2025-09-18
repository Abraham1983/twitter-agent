#!/usr/bin/env python3
import schedule
import time
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.monitoring_agent import MonitoringAgent

def run_engagement_monitoring():
    """Run the engagement monitoring check"""
    print(f"🔍 Running scheduled engagement monitoring - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize the monitoring agent
        monitor = MonitoringAgent()
        
        if monitor.initialize_agent():
            # Check for new mentions
            mentions = monitor.monitor_mentions(max_results=20)
            monitor.process_mentions(mentions)
            
            print("✅ Scheduled engagement monitoring completed successfully!")
        else:
            print("❌ Failed to initialize monitoring agent!")
            
    except Exception as e:
        print(f"❌ Error in scheduled engagement monitoring: {e}")
        import traceback
        traceback.print_exc()

def run_trend_monitoring():
    """Monitor trending topics"""
    print(f"📈 Running scheduled trend monitoring - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize the trend analysis agent
        from agents.trend_analysis_agent import TrendAnalysisAgent
        from utils.database import TwitterDatabase
        
        trend_agent = TrendAnalysisAgent()
        db = TwitterDatabase()
        
        # Get trending topics
        trends = trend_agent.get_trending_hashtags(woeid=23424977)  # US
        
        if "error" not in trends:
            # Save to database
            trends['analysis_type'] = 'hashtag'
            trends['location_name'] = 'United States'
            db.save_trend_analysis(trends)
            print("✅ Scheduled trend monitoring completed successfully!")
        else:
            print(f"❌ Trend monitoring failed: {trends['error']}")
            
    except Exception as e:
        print(f"❌ Error in scheduled trend monitoring: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main monitoring scheduler function"""
    print("🚀 Starting Twitter Engagement Monitoring Scheduler")
    print("=" * 50)
    
    # Schedule engagement monitoring every 15 minutes
    schedule.every(15).minutes.do(run_engagement_monitoring)
    
    # Schedule trend monitoring every 2 hours
    schedule.every(2).hours.do(run_trend_monitoring)
    
    print("⏰ Scheduled monitoring intervals:")
    print("   • Every 15 minutes - Check for new mentions and engagements")
    print("   • Every 2 hours - Trend monitoring")
    print("\n🕒 Monitoring scheduler is now running... (Press Ctrl+C to stop)")
    
    # Run any pending jobs immediately when starting
    schedule.run_pending()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring scheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Monitoring scheduler error: {e}")
        sys.exit(1)
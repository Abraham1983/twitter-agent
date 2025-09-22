#!/usr/bin/env python3
import schedule
import time
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import TwitterAgentPipeline
from autonomous_monitor import AutonomousMonitor

def run_daily_posting():
    """Run the daily Twitter posting pipeline"""
    print(f"📅 Running scheduled Twitter posting - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize the pipeline
        pipeline = TwitterAgentPipeline()
        
        # Run the daily content pipeline
        success = pipeline.run_daily_content()
        
        if success:
            print("✅ Scheduled posting completed successfully!")
        else:
            print("❌ Scheduled posting failed!")
            # Notify autonomous monitor of failure
            monitor = AutonomousMonitor()
            monitor.post_failure_recovery("Scheduled posting failed - content pipeline returned False")
            
    except Exception as e:
        print(f"❌ Error in scheduled posting: {e}")
        import traceback
        traceback.print_exc()
        
        # Notify autonomous monitor of failure
        monitor = AutonomousMonitor()
        monitor.post_failure_recovery(f"Scheduled posting failed with exception: {str(e)}")

def run_trend_analysis():
    """Analyze trending topics"""
    print(f"🔍 Running scheduled trend analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize the pipeline
        pipeline = TwitterAgentPipeline()
        
        # Analyze trends
        trends = pipeline.analyze_trends()
        
        if trends:
            print("✅ Scheduled trend analysis completed successfully!")
        else:
            print("❌ Scheduled trend analysis failed!")
            
    except Exception as e:
        print(f"❌ Error in scheduled trend analysis: {e}")
        import traceback
        traceback.print_exc()

def run_performance_analysis():
    """Analyze performance metrics"""
    print(f"📊 Running scheduled performance analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize the pipeline
        pipeline = TwitterAgentPipeline()
        
        # Analyze performance
        performance = pipeline.analyze_performance()
        
        if performance:
            print("✅ Scheduled performance analysis completed successfully!")
        else:
            print("❌ Scheduled performance analysis failed!")
            
    except Exception as e:
        print(f"❌ Error in scheduled performance analysis: {e}")
        import traceback
        traceback.print_exc()

def run_proactive_engagement():
    """Proactively engage with target audience"""
    print(f"🤝 Running scheduled proactive engagement - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize the pipeline
        pipeline = TwitterAgentPipeline()
        
        # Proactive engagement
        success = pipeline.proactive_engagement()
        
        if success:
            print("✅ Scheduled proactive engagement completed successfully!")
        else:
            print("❌ Scheduled proactive engagement failed!")
            
    except Exception as e:
        print(f"❌ Error in scheduled proactive engagement: {e}")
        import traceback
        traceback.print_exc()

def run_comment_response():
    """Respond to comments on posted tweets"""
    print(f"💬 Running scheduled comment response - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize the pipeline
        pipeline = TwitterAgentPipeline()
        
        # Respond to comments
        success = pipeline.respond_to_comments()
        
        if success:
            print("✅ Scheduled comment response completed successfully!")
        else:
            print("❌ Scheduled comment response failed!")
            
    except Exception as e:
        print(f"❌ Error in scheduled comment response: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main scheduler function"""
    print("🚀 Starting Twitter Agent Scheduler")
    print("=" * 50)
    
    # Schedule the daily posting for 9:00 AM
    schedule.every().day.at("09:00").do(run_daily_posting)
    
    # Also schedule for 3:00 PM as a second daily post
    schedule.every().day.at("15:00").do(run_daily_posting)
    
    # Schedule trend analysis once per day at 10:00 AM
    schedule.every().day.at("10:00").do(run_trend_analysis)
    
    # Schedule performance analysis daily at 11:00 PM
    schedule.every().day.at("23:00").do(run_performance_analysis)
    
    # Schedule proactive engagement every 4 hours
    schedule.every(4).hours.do(run_proactive_engagement)
    
    # Schedule comment response once per day at 8:00 PM
    schedule.every().day.at("20:00").do(run_comment_response)
    
    print("⏰ Scheduled tasks:")
    print("   • 9:00 AM - Morning post")
    print("   • 3:00 PM - Afternoon post")
    print("   • 10:00 AM - Daily trend analysis")
    print("   • 11:00 PM - Daily performance analysis")
    print("   • Every 4 hours - Proactive engagement")
    print("   • 8:00 PM - Daily comment response")
    print("\n🕒 Scheduler is now running... (Press Ctrl+C to stop)")
    
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
        print("\n🛑 Scheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Scheduler error: {e}")
        sys.exit(1)
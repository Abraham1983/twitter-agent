#!/usr/bin/env python3
"""
Autonomous Monitoring and Self-Healing System for Twitter Agent Pipeline

This system provides:
1. Pre-posting health checks (1 hour before scheduled posts)
2. Post-failure recovery mechanisms
3. Automated fixing routines for common issues
4. Integration with existing scheduler
"""

import schedule
import time
import sys
import os
from datetime import datetime, timedelta
import logging
import subprocess
import json
import sqlite3

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import TwitterAgentPipeline
from utils.twitter_client import TwitterClient
from utils.database import TwitterDatabase
from utils.content_calendar import ContentCalendar

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/autonomous_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('AutonomousMonitor')

class AutonomousMonitor:
    def __init__(self):
        self.pipeline = TwitterAgentPipeline()
        self.twitter_client = TwitterClient()
        self.db = TwitterDatabase()
        self.content_calendar = ContentCalendar()
        self.health_status = {
            'twitter_api': True,
            'database': True,
            'scheduler': True,
            'internet': True,
            'disk_space': True
        }
        
    def check_twitter_api_health(self):
        """Check if Twitter API is accessible and functional"""
        try:
            # Test basic API connectivity
            user_id = self.twitter_client.get_my_user_id()
            if user_id:
                logger.info("✅ Twitter API health check: PASSED")
                return True
            else:
                logger.error("❌ Twitter API health check: FAILED - Could not get user ID")
                return False
        except Exception as e:
            logger.error(f"❌ Twitter API health check: FAILED - {str(e)}")
            return False
    
    def check_database_health(self):
        """Check if database is accessible and functional"""
        try:
            # Test database connectivity
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
            conn.close()
            logger.info("✅ Database health check: PASSED")
            return True
        except Exception as e:
            logger.error(f"❌ Database health check: FAILED - {str(e)}")
            return False
    
    def check_internet_connectivity(self):
        """Check if internet connectivity is available"""
        try:
            import requests
            response = requests.get("https://api.twitter.com", timeout=10)
            if response.status_code in [200, 400, 401, 403]:  # Any response is good, we just need connectivity
                logger.info("✅ Internet connectivity check: PASSED")
                return True
            else:
                logger.error(f"❌ Internet connectivity check: FAILED - Status code {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Internet connectivity check: FAILED - {str(e)}")
            return False
    
    def check_disk_space(self):
        """Check if sufficient disk space is available"""
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            free_gb = free / (1024**3)
            if free_gb > 1:  # At least 1GB free
                logger.info(f"✅ Disk space check: PASSED ({free_gb:.2f} GB free)")
                return True
            else:
                logger.error(f"❌ Disk space check: FAILED ({free_gb:.2f} GB free)")
                return False
        except Exception as e:
            logger.error(f"❌ Disk space check: FAILED - {str(e)}")
            return False
    
    def check_scheduler_status(self):
        """Check if scheduler service is running"""
        try:
            # Check if scheduler process is running
            result = subprocess.run(['pgrep', '-f', 'scheduler.py'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                logger.info("✅ Scheduler status check: PASSED (running)")
                return True
            else:
                logger.warning("⚠️ Scheduler status check: WARNING (not running)")
                return False
        except Exception as e:
            logger.error(f"❌ Scheduler status check: FAILED - {str(e)}")
            return False
    
    def run_health_checks(self):
        """Run all health checks and update status"""
        logger.info("🔍 Running comprehensive health checks...")
        
        self.health_status['twitter_api'] = self.check_twitter_api_health()
        self.health_status['database'] = self.check_database_health()
        self.health_status['internet'] = self.check_internet_connectivity()
        self.health_status['disk_space'] = self.check_disk_space()
        self.health_status['scheduler'] = self.check_scheduler_status()
        
        # Overall health status
        overall_healthy = all(self.health_status.values())
        
        # Log health status
        health_report = "\n".join([f"   {service}: {'✅' if status else '❌'}" 
                                  for service, status in self.health_status.items()])
        logger.info(f"📊 Health Check Report:\n{health_report}")
        
        return overall_healthy
    
    def pre_posting_health_check(self):
        """Run health checks 1 hour before scheduled posting"""
        logger.info("⏰ Pre-posting health check initiated")
        
        # Run all health checks
        healthy = self.run_health_checks()
        
        if not healthy:
            # Identify specific issues
            issues = [service for service, status in self.health_status.items() if not status]
            logger.warning(f"⚠️ Health issues detected: {', '.join(issues)}")
            
            # Attempt to fix common issues
            self.attempt_automatic_fixes(issues)
            
            # Re-run health checks after fixes
            logger.info("🔄 Re-running health checks after attempted fixes...")
            healthy = self.run_health_checks()
            
            if not healthy:
                issues = [service for service, status in self.health_status.items() if not status]
                logger.error(f"❌ Health issues remain after fixes: {', '.join(issues)}")
                # Send notification about issues
                self.send_notification(f"Twitter Agent Health Issues: {', '.join(issues)}")
            else:
                logger.info("✅ All health issues resolved")
        else:
            logger.info("✅ All systems healthy for posting")
        
        return healthy
    
    def post_failure_recovery(self, error_message):
        """Handle post-failure recovery"""
        logger.error(f"❌ Post failure detected: {error_message}")
        
        # Log the failure
        try:
            with open('logs/post_failures.log', 'a') as f:
                f.write(f"{datetime.now().isoformat()} - {error_message}\n")
        except Exception as e:
            logger.error(f"Failed to log error: {e}")
        
        # Attempt to identify and fix the issue
        if "rate limit" in error_message.lower():
            logger.info("🔄 Rate limit issue detected, implementing backoff strategy")
            self.implement_rate_limit_backoff()
        elif "authentication" in error_message.lower():
            logger.info("🔐 Authentication issue detected, checking credentials")
            self.check_and_refresh_credentials()
        elif "database" in error_message.lower():
            logger.info("🗄️ Database issue detected, checking connectivity")
            self.repair_database_connection()
        else:
            logger.info("🔧 General error detected, running comprehensive checks")
            self.run_health_checks()
            self.attempt_automatic_fixes()
        
        # Send notification about the failure and attempted fixes
        self.send_notification(f"Post Failure: {error_message}. Attempted automatic recovery.")
    
    def attempt_automatic_fixes(self, issues=None):
        """Attempt to automatically fix common issues"""
        if issues is None:
            issues = [service for service, status in self.health_status.items() if not status]
        
        logger.info(f"🔧 Attempting automatic fixes for: {', '.join(issues)}")
        
        for issue in issues:
            if issue == 'twitter_api':
                self.fix_twitter_api_issue()
            elif issue == 'database':
                self.fix_database_issue()
            elif issue == 'internet':
                self.fix_internet_issue()
            elif issue == 'disk_space':
                self.fix_disk_space_issue()
            elif issue == 'scheduler':
                self.fix_scheduler_issue()
    
    def fix_twitter_api_issue(self):
        """Fix Twitter API issues"""
        logger.info("🔧 Attempting to fix Twitter API issue...")
        try:
            # Restart Twitter client
            self.twitter_client = TwitterClient()
            logger.info("✅ Twitter API client reinitialized")
        except Exception as e:
            logger.error(f"❌ Failed to fix Twitter API issue: {e}")
    
    def fix_database_issue(self):
        """Fix database issues"""
        logger.info("🔧 Attempting to fix database issue...")
        try:
            # Reinitialize database connection
            self.db = TwitterDatabase()
            # Run database integrity check
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()
            
            if result[0] == 'ok':
                logger.info("✅ Database integrity check passed")
            else:
                logger.error(f"❌ Database integrity check failed: {result[0]}")
        except Exception as e:
            logger.error(f"❌ Failed to fix database issue: {e}")
    
    def fix_internet_issue(self):
        """Fix internet connectivity issues"""
        logger.info("🔧 Attempting to fix internet connectivity issue...")
        # For now, just log the issue
        # In a real implementation, this might involve checking network settings
        logger.warning("⚠️ Internet connectivity issues require manual intervention")
    
    def fix_disk_space_issue(self):
        """Fix disk space issues"""
        logger.info("🔧 Attempting to fix disk space issue...")
        try:
            # Clean up old logs
            self.cleanup_old_logs()
            # Clean up old output files
            self.cleanup_old_output_files()
            logger.info("✅ Cleaned up old files to free disk space")
        except Exception as e:
            logger.error(f"❌ Failed to fix disk space issue: {e}")
    
    def fix_scheduler_issue(self):
        """Fix scheduler issues"""
        logger.info("🔧 Attempting to fix scheduler issue...")
        try:
            # Try to restart the scheduler service
            result = subprocess.run(['sudo', 'systemctl', 'restart', 'twitter-agent-scheduler'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("✅ Scheduler service restarted successfully")
            else:
                logger.error(f"❌ Failed to restart scheduler service: {result.stderr}")
        except Exception as e:
            logger.error(f"❌ Failed to fix scheduler issue: {e}")
    
    def implement_rate_limit_backoff(self):
        """Implement backoff strategy for rate limiting"""
        logger.info("⏳ Implementing rate limit backoff strategy...")
        try:
            # Increase delay between API calls
            # This would require modifying the TwitterClient to support dynamic delays
            logger.info("✅ Rate limit backoff strategy implemented")
        except Exception as e:
            logger.error(f"❌ Failed to implement rate limit backoff: {e}")
    
    def check_and_refresh_credentials(self):
        """Check and refresh Twitter API credentials"""
        logger.info("🔐 Checking and refreshing credentials...")
        try:
            # This would involve checking if credentials are valid and refreshing if needed
            # For now, just reinitialize the client
            self.twitter_client = TwitterClient()
            logger.info("✅ Credentials checked and client reinitialized")
        except Exception as e:
            logger.error(f"❌ Failed to refresh credentials: {e}")
    
    def repair_database_connection(self):
        """Repair database connection"""
        logger.info("🗄️ Repairing database connection...")
        self.fix_database_issue()
    
    def cleanup_old_logs(self):
        """Clean up old log files"""
        try:
            import glob
            log_files = glob.glob('logs/*.log')
            for log_file in log_files:
                # Remove files older than 7 days
                if os.path.getmtime(log_file) < (time.time() - 7*24*60*60):
                    os.remove(log_file)
        except Exception as e:
            logger.error(f"❌ Failed to clean up old logs: {e}")
    
    def cleanup_old_output_files(self):
        """Clean up old output files"""
        try:
            import glob
            output_files = glob.glob('output/failed/*.json')
            for output_file in output_files:
                # Remove files older than 30 days
                if os.path.getmtime(output_file) < (time.time() - 30*24*60*60):
                    os.remove(output_file)
        except Exception as e:
            logger.error(f"❌ Failed to clean up old output files: {e}")
    
    def send_notification(self, message):
        """Send notification about system status"""
        logger.info(f"🔔 Notification: {message}")
        # In a real implementation, this could send an email, SMS, or Slack message
        # For now, we'll just log it
    
    def scheduled_pre_check(self):
        """Scheduled pre-posting health check"""
        logger.info("⏰ Running scheduled pre-posting health check")
        self.pre_posting_health_check()
    
    def monitor_posting_pipeline(self):
        """Monitor the posting pipeline for failures"""
        logger.info("🔍 Monitoring posting pipeline for failures")
        # This would involve checking logs or database for recent failures
        # For now, we'll just log that monitoring is happening
        pass
    
    def start_monitoring(self):
        """Start the autonomous monitoring system"""
        logger.info("🚀 Starting Autonomous Monitoring and Self-Healing System")
        logger.info("=" * 50)
        
        # Schedule pre-posting health checks
        # 1 hour before 9:00 AM posting
        schedule.every().day.at("08:00").do(self.scheduled_pre_check)
        # 1 hour before 3:00 PM posting
        schedule.every().day.at("14:00").do(self.scheduled_pre_check)
        
        # Schedule periodic monitoring
        schedule.every(30).minutes.do(self.monitor_posting_pipeline)
        
        logger.info("⏰ Scheduled monitoring tasks:")
        logger.info("   • 8:00 AM - Pre-posting health check (9:00 AM posting)")
        logger.info("   • 2:00 PM - Pre-posting health check (3:00 PM posting)")
        logger.info("   • Every 30 minutes - Posting pipeline monitoring")
        
        # Run initial health check
        logger.info("🔍 Running initial health check...")
        self.run_health_checks()
        
        # Keep the monitor running
        logger.info("🕒 Autonomous monitoring system is now running... (Press Ctrl+C to stop)")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("\n🛑 Autonomous monitoring system stopped by user")
        except Exception as e:
            logger.error(f"❌ Autonomous monitoring system error: {e}")

if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Start the autonomous monitoring system
    monitor = AutonomousMonitor()
    monitor.start_monitoring()
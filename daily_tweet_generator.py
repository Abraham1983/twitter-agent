#!/usr/bin/env python3
"""
Daily AutonomIQ Twitter Content Generator
Run this script each day to generate and post your Twitter content.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import TwitterAgentPipeline
from utils.daily_reminder import DailyReminder

def main():
    print("🚀 AutonomIQ Daily Twitter Content Generator")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = TwitterAgentPipeline()
    
    # Show today's reminder context
    reminder = DailyReminder()
    print("\n📋 Today's Context:")
    print(reminder.get_reminder_prompt())
    
    # Show today's planned content
    print("\n📅 Today's Content Plan:")
    today_plan = pipeline.content_calendar.get_today_content()
    print(f"   Type: {today_plan['type']}")
    print(f"   Topic: {today_plan['topic']}")
    
    if pipeline.content_calendar.is_thread_day():
        thread_topic = pipeline.content_calendar.get_thread_topic()
        print(f"   🧵 THREAD DAY: {thread_topic}")
    
    # Ask user if they want to proceed
    print("\n❓ Would you like to generate and post today's content? (y/N): ", end="")
    response = input().strip().lower()
    
    if response in ['y', 'yes']:
        print("\n🎯 Generating content...")
        success = pipeline.run_daily_content()
        
        if success:
            print("\n🎉 Content generated and posted successfully!")
        else:
            print("\n⚠️  Content generation failed or needs manual review")
    else:
        print("\nℹ️  Skipped content generation")

if __name__ == "__main__":
    main()
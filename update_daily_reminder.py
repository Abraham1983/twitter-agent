#!/usr/bin/env python3
"""
Daily Reminder Update Script for AutonomIQ
Run this script each morning to update your daily focus for Twitter content.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.daily_reminder import DailyReminder

def main():
    reminder = DailyReminder()
    
    print("=== AutonomIQ Daily Reminder Update ===")
    print("Press Enter to keep current values, or type new values")
    print()
    
    # Get current reminder
    current = reminder.get_todays_reminder()
    
    # Update daily focus
    current_focus = current.get('daily_focus', '')
    print(f"Current Daily Focus: {current_focus}")
    new_focus = input("New Daily Focus (or Enter to keep current): ").strip()
    
    # Update today's tasks
    print("\nToday's Tasks:")
    current_tasks = current.get('today_tasks', [])
    for i, task in enumerate(current_tasks, 1):
        print(f"  {i}. {task}")
    
    print("\nEnter new tasks (one per line, empty line to finish):")
    new_tasks = []
    while True:
        task = input(f"  {len(new_tasks)+1}. ").strip()
        if not task:
            break
        new_tasks.append(task)
    
    # Update recent learnings
    print("\nRecent Learnings:")
    current_learnings = current.get('recent_learnings', [])
    for i, learning in enumerate(current_learnings, 1):
        print(f"  {i}. {learning}")
    
    print("\nEnter new learnings (one per line, empty line to finish):")
    new_learnings = []
    while True:
        learning = input(f"  {len(new_learnings)+1}. ").strip()
        if not learning:
            break
        new_learnings.append(learning)
    
    # Update reminder
    update_params = {}
    if new_focus:
        update_params['daily_focus'] = new_focus
    if new_tasks:
        update_params['today_tasks'] = new_tasks
    if new_learnings:
        update_params['recent_learnings'] = new_learnings
    
    if update_params:
        if reminder.update_reminder(**update_params):
            print("\n✅ Daily reminder updated successfully!")
        else:
            print("\n❌ Failed to update daily reminder")
    else:
        print("\nℹ️  No changes made")
    
    print("\n=== Current Reminder Context ===")
    print(reminder.get_reminder_prompt())

if __name__ == "__main__":
    main()
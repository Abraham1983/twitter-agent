import os
import json
from datetime import datetime

class DailyReminder:
    def __init__(self, reminder_file="data/daily_reminder.json"):
        self.reminder_file = reminder_file
        os.makedirs(os.path.dirname(reminder_file), exist_ok=True)
        self.init_reminder_file()
    
    def init_reminder_file(self):
        """Initialize reminder file if it doesn't exist"""
        if not os.path.exists(self.reminder_file):
            default_reminder = {
                "last_updated": datetime.now().isoformat(),
                "daily_focus": "Building AutonomIQ - AI automation platform for small businesses",
                "today_tasks": [
                    "Develop new AI agent workflows",
                    "Test voice automation integrations",
                    "Improve client onboarding process"
                ],
                "recent_learnings": [
                    "New workflow optimization technique with n8n",
                    "Better error handling in Retell.ai integrations"
                ]
            }
            with open(self.reminder_file, 'w') as f:
                json.dump(default_reminder, f, indent=2)
    
    def get_todays_reminder(self):
        """Get today's reminder context"""
        try:
            with open(self.reminder_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading reminder file: {e}")
            return {}
    
    def update_reminder(self, daily_focus=None, today_tasks=None, recent_learnings=None):
        """Update today's reminder"""
        reminder = self.get_todays_reminder()
        
        if daily_focus:
            reminder["daily_focus"] = daily_focus
        if today_tasks:
            reminder["today_tasks"] = today_tasks
        if recent_learnings:
            reminder["recent_learnings"] = recent_learnings
            
        reminder["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(self.reminder_file, 'w') as f:
                json.dump(reminder, f, indent=2)
            return True
        except Exception as e:
            print(f"Error updating reminder file: {e}")
            return False
    
    def get_reminder_prompt(self):
        """Get a formatted prompt with today's reminder context"""
        reminder = self.get_todays_reminder()
        
        prompt = "Today's context for AutonomIQ development:\n"
        prompt += f"Daily Focus: {reminder.get('daily_focus', 'Building AutonomIQ platform')}\n\n"
        
        tasks = reminder.get('today_tasks', [])
        if tasks:
            prompt += "Today's Tasks:\n"
            for i, task in enumerate(tasks, 1):
                prompt += f"  {i}. {task}\n"
        
        learnings = reminder.get('recent_learnings', [])
        if learnings:
            prompt += "\nRecent Learnings:\n"
            for i, learning in enumerate(learnings, 1):
                prompt += f"  {i}. {learning}\n"
        
        return prompt
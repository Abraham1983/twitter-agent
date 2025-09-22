from datetime import datetime, timedelta
import json
import os

class ContentCalendar:
    def __init__(self):
        # Your 30-day strategic calendar for AutonomIQ
        self.daily_topics = {
            1: {"type": "personal_journey", "topic": "Day 1 of building AutonomIQ - setting up the foundation"},
            2: {"type": "education_explainer", "topic": "What exactly is AI automation for small businesses"},
            3: {"type": "hot_take_opinion", "topic": "Why most AI tools fail small businesses - they're built for enterprises"},
            4: {"type": "visual_framework", "topic": "AutonomIQ Service Architecture - how we automate businesses"},
            5: {"type": "engagement_booster", "topic": "What repetitive task would you automate first?"},
            6: {"type": "education_explainer", "topic": "Retell.ai + n8n - our voice automation stack explained"},
            7: {"type": "personal_journey", "topic": "Week 1 with AutonomIQ - first client onboarding experience"},
            8: {"type": "education_explainer", "topic": "Workflow automation with n8n - what you can build"},
            9: {"type": "engagement_booster", "topic": "AI agent scheduling meetings gone wrong - humor"},
            10: {"type": "hot_take_opinion", "topic": "Most underrated skill for AI automation - process mapping"},
            11: {"type": "experiment_case_study", "topic": "Built lead capture agent with 85% accuracy"},
            12: {"type": "visual_framework", "topic": "3 Layers of AutonomIQ Automation Framework"},
            13: {"type": "engagement_booster", "topic": "Poll - what's your biggest business pain point?"},
            14: {"type": "hot_take_opinion", "topic": "AI automation won't replace jobs - it'll eliminate busywork"},
            15: {"type": "education_explainer", "topic": "5 Free Tools to Start Automating Your Business Today"},
            16: {"type": "personal_journey", "topic": "Connecting with AI creators - learning from the community"},
            17: {"type": "hot_take_opinion", "topic": "First profitable AI agents will handle scheduling & support"},
            18: {"type": "visual_framework", "topic": "AutonomIQ Starter vs Growth vs Concierge Packages"},
            19: {"type": "engagement_booster", "topic": "Planning AutonomIQ tutorial series - what would help?"},
            20: {"type": "engagement_booster", "topic": "When your AI agent misunderstands a client - funny stories"},
            21: {"type": "experiment_case_study", "topic": "Tested AI content scheduler - here are the results"},
            22: {"type": "education_explainer", "topic": "AI Automation Trends for Small Businesses in 2025"},
            23: {"type": "hot_take_opinion", "topic": "Want better AI results? Focus on data quality first"},
            24: {"type": "engagement_booster", "topic": "What AutonomIQ feature should we build next?"},
            25: {"type": "visual_framework", "topic": "How AutonomIQ Integrates with Your Business Tools"},
            26: {"type": "hot_take_opinion", "topic": "Within 12 months AI agents will handle 50% of client calls"},
            27: {"type": "education_explainer", "topic": "7 Prompts for Better Business Automation Results"},
            28: {"type": "engagement_booster", "topic": "When your automation breaks at the worst time - stories"},
            29: {"type": "personal_journey", "topic": "Month 1 with AutonomIQ - lessons learned, next steps"},
            30: {"type": "personal_journey", "topic": "Month 2 preview - scaling our automation services"}
        }

        # Weekly thread topics (every 7 days)
        self.weekly_threads = {
            7: "Complete beginner's guide to AI automation for small business",
            14: "AutonomIQ case studies - real client results",
            21: "AI automation tools comparison for SMBs",
            28: "Month recap and next month preview for AutonomIQ"
        }
        
        # Track strategy progress
        self.strategy_progress_file = "data/strategy_progress.json"
        self.init_strategy_tracking()

    def init_strategy_tracking(self):
        """Initialize strategy tracking file"""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.strategy_progress_file):
            progress_data = {
                "start_date": datetime.now().isoformat(),
                "current_day": 1,
                "completed_days": []
            }
            with open(self.strategy_progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)

    def get_current_strategy_day(self):
        """Get current day in your 30-day strategy"""
        try:
            with open(self.strategy_progress_file, 'r') as f:
                progress = json.load(f)
            return progress.get("current_day", 1)
        except:
            return 1

    def advance_strategy_day(self):
        """Move to next day in strategy"""
        try:
            with open(self.strategy_progress_file, 'r') as f:
                progress = json.load(f)
            
            current_day = progress.get("current_day", 1)
            progress["current_day"] = min(current_day + 1, 30)
            progress["completed_days"].append(current_day)
            progress["last_updated"] = datetime.now().isoformat()
            
            with open(self.strategy_progress_file, 'w') as f:
                json.dump(progress, f, indent=2)
                
        except Exception as e:
            print(f"Error advancing strategy day: {e}")

    def get_today_content(self):
        """Get today's content based on strategy progress"""
        strategy_day = self.get_current_strategy_day()
        
        return self.daily_topics.get(strategy_day, {
            "type": "education_explainer",
            "topic": "AI automation tip for businesses"
        })

    def get_content_for_day(self, day):
        """Get content for specific strategy day"""
        if day > 30:
            day = ((day - 1) % 30) + 1
            
        return self.daily_topics.get(day, {
            "type": "education_explainer",
            "topic": "AI automation insight"
        })

    def is_thread_day(self, day=None):
        """Check if today should be a thread day"""
        if day is None:
            day = self.get_current_strategy_day()
            
        return day in self.weekly_threads

    def get_thread_topic(self, day=None):
        """Get thread topic for thread days"""
        if day is None:
            day = self.get_current_strategy_day()
            
        return self.weekly_threads.get(day, "AI automation deep dive")

    def get_week_preview(self):
        """Get this week's content preview"""
        current_day = self.get_current_strategy_day()
        week_content = []
        
        for i in range(7):
            day = current_day + i
            if day > 30:
                day = ((day - 1) % 30) + 1
            content = self.get_content_for_day(day)
            week_content.append(f"Strategy Day {day}: {content['type']} - {content['topic']}")
        
        return week_content

    def get_strategy_status(self):
        """Get current strategy status"""
        try:
            with open(self.strategy_progress_file, 'r') as f:
                progress = json.load(f)
            
            current_day = progress.get("current_day", 1)
            completed_days = len(progress.get("completed_days", []))
            start_date = progress.get("start_date", "")
            
            return {
                "current_day": current_day,
                "completed_days": completed_days,
                "remaining_days": 30 - current_day + 1,
                "start_date": start_date,
                "progress_percentage": (completed_days / 30) * 100
            }
        except:
            return {"current_day": 1, "completed_days": 0, "remaining_days": 30}

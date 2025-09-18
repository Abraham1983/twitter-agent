from datetime import datetime, timedelta
import json
import os

class ContentCalendar:
    def __init__(self):
        # Your 30-day strategic calendar
        self.daily_topics = {
            1: {"type": "personal_journey", "topic": "Starting AI automation journey - documenting everything"},
            2: {"type": "education_explainer", "topic": "What exactly IS an AI agent - simple breakdown"},
            3: {"type": "hot_take_opinion", "topic": "People overestimate AI now but underestimate agents in 2-3 years"},
            4: {"type": "visual_framework", "topic": "Flow of an AI Agent - simple diagram"},
            5: {"type": "engagement_booster", "topic": "Coolest AI project you've seen this month"},
            6: {"type": "education_explainer", "topic": "LLMs vs Agents - brain vs brain + memory + tools + actions"},
            7: {"type": "personal_journey", "topic": "Small goal - 1000 followers in 90 days documenting AI journey"},
            8: {"type": "education_explainer", "topic": "LangChain explained - what it is and what you can build"},
            9: {"type": "engagement_booster", "topic": "AI agent ordering groceries gone wrong - humor"},
            10: {"type": "hot_take_opinion", "topic": "Most underrated AI skill - prompt chaining"},
            11: {"type": "experiment_case_study", "topic": "Built simple agent to auto-summarize emails"},
            12: {"type": "visual_framework", "topic": "4 Layers of AI Agent Systems framework"},
            13: {"type": "engagement_booster", "topic": "Poll - will agents replace 50% jobs in 5 years"},
            14: {"type": "hot_take_opinion", "topic": "AI agents won't replace jobs directly - they'll reshape them"},
            15: {"type": "education_explainer", "topic": "10 Free AI Tools to Experiment With Agents Today"},
            16: {"type": "personal_journey", "topic": "Spending time replying to big AI creators today"},
            17: {"type": "hot_take_opinion", "topic": "First profitable agents will be boring - support, scheduling, research"},
            18: {"type": "visual_framework", "topic": "AI Assistant vs AI Agent comparison chart"},
            19: {"type": "engagement_booster", "topic": "Planning AI tutorial thread - what would help you most"},
            20: {"type": "engagement_booster", "topic": "Agent having existential crisis waiting for API call - humor"},
            21: {"type": "experiment_case_study", "topic": "Tested running agent to draft tweets - here are outputs"},
            22: {"type": "education_explainer", "topic": "AI Agents Will Be 2025's Biggest Disruption - 7 industries"},
            23: {"type": "hot_take_opinion", "topic": "Want your AI agent to feel 2x smarter - give it memory"},
            24: {"type": "engagement_booster", "topic": "What AI agent experiment should I try next"},
            25: {"type": "visual_framework", "topic": "How AI agents interact with APIs diagram"},
            26: {"type": "hot_take_opinion", "topic": "Within 12 months people will trust AI agents with calendar more than humans"},
            27: {"type": "education_explainer", "topic": "5 Prompts to Spark Agent Behaviors cheat sheet"},
            28: {"type": "engagement_booster", "topic": "When your AI agent hallucinates but you're too tired to debug - humor"},
            29: {"type": "personal_journey", "topic": "Twitter recap - 30 days in, what I learned building agents"},
            30: {"type": "personal_journey", "topic": "Month 2 preview - bigger experiments, deeper threads"}
        }

        # Weekly thread topics (every 7 days)
        self.weekly_threads = {
            7: "Complete beginner's guide to AI agents",
            14: "Business automation case studies compilation",
            21: "AI agent frameworks comparison and guide",
            28: "Month recap and next month preview"
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

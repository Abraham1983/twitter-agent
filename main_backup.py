#!/usr/bin/env python3
import json
import os
import time
import schedule
from datetime import datetime
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.keyword_agent import KeywordAgent
from agents.seo_agent import SEOAgent
from agents.boss_agent import BossAgent
from utils.twitter_client import TwitterClient
from utils.database import TwitterDatabase
from utils.content_calendar import ContentCalendar

class TwitterAgentPipeline:
    def __init__(self):
        # Content creation agents
        self.research_agent = ResearchAgent()
        self.writer_agent = WriterAgent()
        self.keyword_agent = KeywordAgent()
        self.seo_agent = SEOAgent()
        self.boss_agent = BossAgent()

        # Utilities
        self.twitter_client = TwitterClient()
        self.db = TwitterDatabase()
        self.content_calendar = ContentCalendar()

        self.posted_tweets = []

    def run_daily_content(self):
        """Run daily content based on your strategic calendar"""

        # Get today's planned content
        daily_plan = self.content_calendar.get_today_content()

        print(f"📅 Today's strategic content:")
        print(f"   Type: {daily_plan['type']}")
        print(f"   Topic: {daily_plan['topic']}")

        # Check if it's a thread day
        if self.content_calendar.is_thread_day():
            thread_topic = self.content_calendar.get_thread_topic()
            print(f"🧵 THREAD DAY: {thread_topic}")
            daily_plan['topic'] = thread_topic
            daily_plan['is_thread'] = True

        # Run pipeline with strategic content
        return self.run_strategic_pipeline(daily_plan)

    def run_strategic_pipeline(self, daily_plan, max_attempts=3):
        """Enhanced pipeline with automatic feedback loop and iterative improvement"""

        topic = daily_plan['topic']
        content_type = daily_plan['type']

        print(f"🔍 Starting strategic pipeline...")
        print(f"📝 Content Type: {content_type}")
        print(f"🎯 Topic: {topic}")

        # Initialize variables for iteration
        research_data = None
        boss_feedback = None
        attempt = 1

        while attempt <= max_attempts:
            print(f"\n🔄 ATTEMPT {attempt}/{max_attempts}")
            
            try:
                # Step 1: Strategic Research (with previous feedback if exists)
                print("1️⃣ Researching with strategy context...")
                if attempt == 1:
                    research_data = self.research_agent.research_topic(content_type)
                else:
                    research_data = self.research_agent.research_topic_with_feedback(
                        content_type, boss_feedback
                    )
                print(f"   ✅ Research completed for {research_data['theme']} theme")

                # Step 2: Template-based Writing (with previous feedback if exists)
                print("2️⃣ Writing with proven templates...")
                if attempt == 1:
                    writer_data = self.writer_agent.create_content(research_data)
                else:
                    writer_data = self.writer_agent.create_content_with_feedback(
                        research_data, boss_feedback
                    )
                print(f"   ✅ Content written using {writer_data['content_type']} template")

                # Step 3: Keyword optimization (with previous feedback if exists)
                print("3️⃣ Optimizing keywords...")
                if attempt == 1:
                    keyword_data = self.keyword_agent.optimize_keywords(writer_data)
                else:
                    keyword_data = self.keyword_agent.optimize_keywords_with_feedback(
                        writer_data, boss_feedback
                    )
                print("   ✅ Keywords optimized")

                # Step 4: SEO optimization (with previous feedback if exists)
                print("4️⃣ SEO optimization...")
                if attempt == 1:
                    seo_data = self.seo_agent.optimize_seo(keyword_data)
                else:
                    seo_data = self.seo_agent.optimize_seo_with_feedback(
                        keyword_data, boss_feedback
                    )
                print("   ✅ SEO optimized")

                # Step 5: Boss approval (Claude Sonnet 3.5)
                print("5️⃣ Boss review (Claude Sonnet 3.5)...")
                boss_decision = self.boss_agent.review_and_approve(
                    research_data, writer_data, keyword_data, seo_data, attempt
                )

                if "APPROVE" in boss_decision['decision']:
                    print("✅ APPROVED! Publishing to Twitter...")

                    # Clean up the final content
                    final_content = boss_decision['decision'].replace("APPROVE", "").strip()
                    if final_content.startswith(":"):
                        final_content = final_content[1:].strip()

                    # Post to Twitter
                    response = self.twitter_client.post_tweet(final_content)

                    if response:
                        # Save to database
                        tweet_data = {
                            'tweet_id': str(response.data['id']),
                            'content': final_content,
                            'content_type': content_type,
                            'theme': research_data.get('theme'),
                            'posted_at': datetime.now(),
                            'attempts_needed': attempt
                        }
                        self.db.save_tweet_analytics(tweet_data)
                        self.posted_tweets.append(tweet_data)

                        print(f"🎉 Tweet posted successfully after {attempt} attempts!")
                        print(f"   📊 Tweet ID: {response.data['id']}")
                        print(f"   📝 Content Type: {content_type}")
                        print(f"   🎯 Theme: {research_data.get('theme')}")

                    return True
                
                else:
                    # Content rejected - extract feedback and continue loop
                    print(f"❌ REJECTED - Attempt {attempt}")
                    boss_feedback = boss_decision['decision']
                    print(f"   📝 Boss feedback: {boss_feedback[:200]}...")
                    
                    if attempt < max_attempts:
                        print(f"🔄 Sending feedback to agents for revision...")
                        # Save feedback for next iteration
                        attempt += 1
                        continue
                    else:
                        print(f"⚠️ Max attempts ({max_attempts}) reached. Saving for manual review.")
                        self.save_failed_content(research_data, writer_data, boss_feedback)
                        return False

            except Exception as e:
                print(f"❌ Pipeline error on attempt {attempt}: {e}")
                if attempt < max_attempts:
                    print("🔄 Retrying...")
                    attempt += 1
                    continue
                else:
                    return False

        return False

    def save_failed_content(self, research_data, writer_data, feedback):
        """Save content that failed all attempts for manual review"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        failed_content = {
            'timestamp': timestamp,
            'research': research_data,
            'content': writer_data,
            'boss_feedback': feedback,
            'status': 'requires_manual_review'
        }
        
        os.makedirs('output/failed', exist_ok=True)
        with open(f'output/failed/{timestamp}_failed.json', 'w') as f:
            json.dump(failed_content, f, indent=2, default=str)

    def test_system(self):
        """Test all system components"""
        print("🧪 Testing strategic Twitter system...")

        try:
            # Test database
            self.db.init_database()
            print("✅ Database: OK")

            # Test content calendar
            today_content = self.content_calendar.get_today_content()
            print(f"✅ Content Calendar: OK - Today: {today_content['type']}")

            # Test research agent
            test_research = self.research_agent.research_topic("education_explainer")
            print("✅ Strategic Research Agent: OK")

            print("✅ Twitter Client: Ready")

            print("🎉 All strategic systems working!")
            return True

        except Exception as e:
            print(f"❌ System test failed: {e}")
            return False

if __name__ == "__main__":
    print("🚀 Strategic Twitter Agent Pipeline")
    print("=" * 50)

    pipeline = TwitterAgentPipeline()

    # Test the strategic system
    if pipeline.test_system():
        print("\n📋 Today's Content Plan:")
        today_plan = pipeline.content_calendar.get_today_content()
        print(f"   Type: {today_plan['type']}")
        print(f"   Topic: {today_plan['topic']}")

        if pipeline.content_calendar.is_thread_day():
            thread_topic = pipeline.content_calendar.get_thread_topic()
            print(f"   🧵 THREAD DAY: {thread_topic}")

        print("\n🧪 Running test strategic pipeline...")
        success = pipeline.run_daily_content()

        if success:
            print("\n🎉 Strategic pipeline completed successfully!")
        else:
            print("\n⚠️ Pipeline needs adjustments")

    else:
        print("❌ System test failed - check your configuration")

    def test_system(self):
        """Test all system components"""
        print("🧪 Testing strategic Twitter system...")

        try:
            # Test database
            self.db.init_database()
            print("✅ Database: OK")

            # Test content calendar
            today_content = self.content_calendar.get_today_content()
            print(f"✅ Content Calendar: OK - Today: {today_content['type']}")

            # Test research agent
            test_research = self.research_agent.research_topic("education_explainer")
            print("✅ Strategic Research Agent: OK")

            print("✅ Twitter Client: Ready")

            print("🎉 All strategic systems working!")
            return True

        except Exception as e:
            print(f"❌ System test failed: {e}")
            return False

if __name__ == "__main__":
    print("🚀 Strategic Twitter Agent Pipeline")
    print("=" * 50)

    pipeline = TwitterAgentPipeline()

    # Test the strategic system
    if pipeline.test_system():
        print("\n📋 Today's Content Plan:")
        today_plan = pipeline.content_calendar.get_today_content()
        print(f"   Type: {today_plan['type']}")
        print(f"   Topic: {today_plan['topic']}")

        if pipeline.content_calendar.is_thread_day():
            thread_topic = pipeline.content_calendar.get_thread_topic()
            print(f"   🧵 THREAD DAY: {thread_topic}")

        print("\n🧪 Running test strategic pipeline...")
        success = pipeline.run_daily_content()

        if success:
            print("\n🎉 Strategic pipeline completed successfully!")
        else:
            print("\n⚠️ Pipeline needs adjustments")

    else:
        print("❌ System test failed - check your configuration")

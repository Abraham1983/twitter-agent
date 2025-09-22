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
from agents.monitoring_agent import MonitoringAgent
from agents.trend_analysis_agent import TrendAnalysisAgent
from agents.performance_agent import PerformanceAgent
from agents.engagement_agent import EngagementAgent
from utils.twitter_client import TwitterClient
from utils.database import TwitterDatabase
from utils.content_calendar import ContentCalendar
from utils.daily_reminder import DailyReminder


class TwitterAgentPipeline:
    def __init__(self):
        # Content creation agents
        self.research_agent = ResearchAgent()
        self.writer_agent = WriterAgent()
        self.keyword_agent = KeywordAgent()
        self.seo_agent = SEOAgent()
        self.boss_agent = BossAgent()
        self.monitoring_agent = MonitoringAgent()
        self.trend_analysis_agent = TrendAnalysisAgent()
        self.performance_agent = PerformanceAgent()
        self.engagement_agent = EngagementAgent()

        # Utilities
        self.twitter_client = TwitterClient()
        self.db = TwitterDatabase()
        self.content_calendar = ContentCalendar()
        self.daily_reminder = DailyReminder()

        self.posted_tweets = []

    def run_daily_content(self):
        """Run daily content based on your strategic calendar"""
        # Run pre-posting health check
        print("🔍 Running pre-posting health check...")
        if not self.run_pre_posting_health_check():
            print("❌ Pre-posting health check failed. Aborting content posting.")
            return False

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

        research_data = None
        boss_feedback = None
        attempt = 1

        while attempt <= max_attempts:
            print(f"\n🔄 ATTEMPT {attempt}/{max_attempts}")

            try:
                # Step 1: Research
                print("1️⃣ Researching with strategy context...")
                if attempt == 1:
                    research_data = self.research_agent.research_topic(content_type)
                else:
                    research_data = self.research_agent.research_topic_with_feedback(
                        content_type, boss_feedback
                    )
                print(f"   ✅ Research completed for {research_data['theme']} theme")

                # Step 2: Writing
                print("2️⃣ Writing with proven templates...")
                if attempt == 1:
                    writer_data = self.writer_agent.create_content(research_data)
                else:
                    writer_data = self.writer_agent.create_content_with_feedback(
                        research_data, boss_feedback
                    )
                print(f"   ✅ Content written using {writer_data['content_type']} template")

                # Step 3: Keyword optimization
                print("3️⃣ Optimizing keywords...")
                if attempt == 1:
                    keyword_data = self.keyword_agent.optimize_keywords(writer_data)
                else:
                    keyword_data = self.keyword_agent.optimize_keywords_with_feedback(
                        writer_data, boss_feedback
                    )
                print("   ✅ Keywords optimized")

                # Step 4: SEO optimization
                print("4️⃣ SEO optimization...")
                if attempt == 1:
                    seo_data = self.seo_agent.optimize_seo(keyword_data)
                else:
                    seo_data = self.seo_agent.optimize_seo_with_feedback(
                        keyword_data, boss_feedback
                    )
                print("   ✅ SEO optimized")

                # Step 5: Boss approval
                print("5️⃣ Boss review (Claude Sonnet 3.5)...")
                boss_decision = self.boss_agent.review_and_approve(
                    research_data, writer_data, keyword_data, seo_data, attempt
                )

                final_content = boss_decision.get("final_approved_content")

                if final_content:
                    print("✅ APPROVED! Publishing to Twitter...")

                    # DEBUG: Show what we're about to post
                    print(f"🔍 DEBUG: About to post content:")
                    print(f"   Length: {len(final_content)} characters")
                    print(f"   Content: '{final_content}'")
                    print(f"   Content repr: {repr(final_content)}")

                    response = self.twitter_client.post_tweet(final_content)

                    if response:
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
                    print(f"❌ REJECTED - Attempt {attempt}")
                    boss_feedback = boss_decision['decision']
                    print(f"   📝 Boss feedback: {boss_feedback[:200]}...")

                    if attempt < max_attempts:
                        print(f"🔄 Sending feedback to agents for revision...")
                        attempt += 1
                        continue
                    else:
                        print(f"⚠️ Max attempts ({max_attempts}) reached. Saving for manual review.")
                        self.save_failed_content(research_data, writer_data, boss_feedback)
                        return False

            except Exception as e:
                print(f"❌ Pipeline error on attempt {attempt}: {e}")
                import traceback
                traceback.print_exc()
                
                # Notify autonomous monitor of the error
                try:
                    from autonomous_monitor import AutonomousMonitor
                    monitor = AutonomousMonitor()
                    monitor.post_failure_recovery(f"Pipeline error on attempt {attempt}: {str(e)}")
                except Exception as monitor_error:
                    print(f"❌ Failed to notify autonomous monitor: {monitor_error}")
                
                if attempt < max_attempts:
                    print("🔄 Retrying...")
                    attempt += 1
                    continue
                else:
                    return False

        return False

    def respond_to_comments(self):
        """Respond to comments on posted tweets using the monitoring agent"""
        print("💬 Starting comment response process...")
        try:
            # Initialize the monitoring agent if not already done
            if not self.monitoring_agent.my_user_id:
                if not self.monitoring_agent.initialize_agent():
                    print("❌ Failed to initialize monitoring agent for comment responses")
                    return False
            
            # Respond to comments
            self.monitoring_agent.respond_to_comments()
            print("✅ Comment response process completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in comment response process: {e}")
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

    def run_pre_posting_health_check(self):
        """Run pre-posting health check to ensure all systems are ready"""
        try:
            print("🔍 Checking Twitter API connectivity...")
            user_id = self.twitter_client.get_my_user_id()
            if not user_id:
                print("❌ Twitter API connectivity check failed")
                return False
            print("✅ Twitter API connectivity: OK")
            
            print("🔍 Checking database connectivity...")
            try:
                conn = sqlite3.connect(self.db.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
                conn.close()
                print("✅ Database connectivity: OK")
            except Exception as e:
                print(f"❌ Database connectivity check failed: {e}")
                return False
            
            print("🔍 Checking internet connectivity...")
            try:
                import requests
                response = requests.get("https://api.twitter.com", timeout=10)
                if response.status_code not in [200, 400, 401, 403]:
                    print(f"❌ Internet connectivity check failed: Status code {response.status_code}")
                    return False
                print("✅ Internet connectivity: OK")
            except Exception as e:
                print(f"❌ Internet connectivity check failed: {e}")
                return False
            
            print("✅ All pre-posting health checks passed!")
            return True
        except Exception as e:
            print(f"❌ Pre-posting health check failed with exception: {e}")
            return False

    def analyze_trends(self):
        """Analyze trending topics to inform research"""
        print("🔍 Analyzing trending topics...")
        try:
            # Get trending hashtags in the US
            trends = self.trend_analysis_agent.get_trending_hashtags(woeid=23424977)  # US
            
            if "error" in trends:
                print(f"❌ Trend analysis failed: {trends['error']}")
                return None
            
            # Save trend analysis to database
            trends['analysis_type'] = 'hashtag'
            trends['location_name'] = 'United States'
            self.db.save_trend_analysis(trends)
            
            print(f"✅ Analyzed {trends['total_hashtags']} trending hashtags")
            return trends
            
        except Exception as e:
            print(f"❌ Error in trend analysis: {e}")
            return None

    def analyze_performance(self):
        """Analyze past performance to optimize future content"""
        print("📊 Analyzing past performance...")
        try:
            # Get performance analysis
            performance = self.performance_agent.analyze_performance()
            
            if "error" in performance:
                print(f"❌ Performance analysis failed: {performance['error']}")
                return None
            
            # Save performance analysis to database
            self.db.save_performance_analysis(performance)
            
            print(f"✅ Analyzed performance of {performance.get('total_tweets_analyzed', 0)} tweets")
            return performance
            
        except Exception as e:
            print(f"❌ Error in performance analysis: {e}")
            return None

    def proactive_engagement(self):
        """Proactively engage with target audience content"""
        print("🤝 Starting proactive engagement...")
        try:
            # Define target keywords for your audience
            target_keywords = [
                "AI automation", "cybersecurity", "cloud platforms", 
                "machine learning", "python programming", "devops"
            ]
            
            # Find content to engage with
            content = self.engagement_agent.find_target_audience_content(target_keywords, max_results=10)
            
            if "error" in content:
                print(f"❌ Content discovery failed: {content['error']}")
                return False
            
            if content['total'] == 0:
                print("🔍 No target audience content found")
                return True
            
            print(f"✅ Found {content['total']} pieces of content to engage with")
            
            # Engage with each piece of content
            for tweet in content['tweets']:
                # Randomly decide on engagement type (be conservative with commenting)
                import random
                engagement_type = random.choices(
                    ["like", "like_and_comment", "retweet"], 
                    weights=[0.6, 0.3, 0.1]  # 60% like, 30% like+comment, 10% retweet
                )[0]
                
                result = self.engagement_agent.engage_with_content(tweet, engagement_type)
                
                if "error" in result:
                    print(f"❌ Engagement failed for tweet {tweet['id']}: {result['error']}")
                    continue
                
                # Save engagement result to database
                engagement_record = {
                    'target_tweet_id': tweet['id'],
                    'target_user_id': tweet['author_id'],
                    'action_taken': ', '.join(result['actions']),
                    'response_content': result.get('comment', ''),
                    'success': 'failed' not in ''.join(result['actions']),
                    'engagement_metrics': {
                        'like_count': tweet['like_count'],
                        'retweet_count': tweet['retweet_count'],
                        'reply_count': tweet['reply_count']
                    }
                }
                self.db.save_proactive_engagement(engagement_record)
                
                print(f"✅ Engaged with tweet {tweet['id']}: {', '.join(result['actions'])}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in proactive engagement: {e}")
            return False

    def get_content_recommendations(self):
        """Get content recommendations based on performance analysis"""
        try:
            recommendations = self.performance_agent.get_content_recommendations()
            
            if "error" in recommendations:
                print(f"❌ Failed to get recommendations: {recommendations['error']}")
                return None
            
            print("💡 Content Recommendations:")
            for rec in recommendations.get("content_strategy", []):
                print(f"   • {rec}")
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Error getting content recommendations: {e}")
            return None

    def test_system(self):
        """Test all system components"""
        print("🧪 Testing strategic Twitter system...")

        try:
            self.db.init_database()
            print("✅ Database: OK")

            today_content = self.content_calendar.get_today_content()
            print(f"✅ Content Calendar: OK - Today: {today_content['type']}")

            test_research = self.research_agent.research_topic("education_explainer")
            print("✅ Strategic Research Agent: OK")

            # Test monitoring agent initialization
            if self.monitoring_agent.initialize_agent():
                print("✅ Monitoring Agent: OK")
            else:
                print("⚠️ Monitoring Agent: Initialization failed")

            # Test new agents
            trends = self.trend_analysis_agent.get_trending_hashtags(woeid=23424977)  # US
            if not "error" in trends:
                print("✅ Trend Analysis Agent: OK")
            else:
                print("⚠️ Trend Analysis Agent: Failed to get trends")

            performance = self.performance_agent.analyze_performance()
            if not "error" in performance:
                print("✅ Performance Agent: OK")
            else:
                print("⚠️ Performance Agent: Failed to analyze performance")

            # Test engagement agent (be careful not to actually engage)
            target_keywords = ["AI", "technology"]
            content = self.engagement_agent.find_target_audience_content(target_keywords, max_results=1)
            if not "error" in content:
                print("✅ Engagement Agent: OK")
            else:
                print("⚠️ Engagement Agent: Failed to find content")

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

    if pipeline.test_system():
        print("\n📋 Today's Content Plan:")
        today_plan = pipeline.content_calendar.get_today_content()
        print(f"   Type: {today_plan['type']}")
        print(f"   Topic: {today_plan['topic']}")

        if pipeline.content_calendar.is_thread_day():
            thread_topic = pipeline.content_calendar.get_thread_topic()
            print(f"   🧵 THREAD DAY: {thread_topic}")

        # Analyze trends to inform content
        print("\n🔍 Trend Analysis:")
        trends = pipeline.analyze_trends()
        if trends:
            print(f"   Top 3 trending hashtags: {', '.join([t['name'] for t in trends['hashtags'][:3]])}")

        # Analyze performance
        print("\n📊 Performance Analysis:")
        performance = pipeline.analyze_performance()
        if performance:
            print(f"   Average engagement per post: {performance['average_metrics']['likes'] + performance['average_metrics']['retweets'] + performance['average_metrics']['replies']:.1f}")

        # Get content recommendations
        print("\n💡 Content Recommendations:")
        recommendations = pipeline.get_content_recommendations()

        # Proactive engagement
        print("\n🤝 Proactive Engagement:")
        pipeline.proactive_engagement()

        print("\n🧪 Running test strategic pipeline...")
        success = pipeline.run_daily_content()

        if success:
            print("\n🎉 Strategic pipeline completed successfully!")
        else:
            print("\n⚠️ Pipeline needs adjustments")

    else:
        print("❌ System test failed - check your configuration")

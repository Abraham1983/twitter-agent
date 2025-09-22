#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import TwitterAgentPipeline
from utils.twitter_client import TwitterClient
from datetime import datetime

def manual_post():
    """Manually post content to ensure something goes out today"""
    print(f"📅 Manual Twitter post - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize the pipeline
    pipeline = TwitterAgentPipeline()
    
    # Get today's planned content
    daily_plan = pipeline.content_calendar.get_today_content()
    
    print(f"📅 Today's strategic content:")
    print(f"   Type: {daily_plan['type']}")
    print(f"   Topic: {daily_plan['topic']}")
    
    # Check if it's a thread day
    if pipeline.content_calendar.is_thread_day():
        thread_topic = pipeline.content_calendar.get_thread_topic()
        print(f"🧵 THREAD DAY: {thread_topic}")
        daily_plan['topic'] = thread_topic
        daily_plan['is_thread'] = True
    
    # Run just the content creation part (without approval loop to save time)
    print("🔍 Starting content creation...")
    
    try:
        # Step 1: Research
        print("1️⃣ Researching...")
        research_data = pipeline.research_agent.research_topic(daily_plan['type'])
        print(f"   ✅ Research completed for {research_data['theme']} theme")
        
        # Step 2: Writing
        print("2️⃣ Writing...")
        writer_data = pipeline.writer_agent.create_content(research_data)
        print(f"   ✅ Content written using {writer_data['content_type']} template")
        
        # Step 3: Keyword optimization
        print("3️⃣ Optimizing keywords...")
        keyword_data = pipeline.keyword_agent.optimize_keywords(writer_data)
        print("   ✅ Keywords optimized")
        
        # Step 4: SEO optimization
        print("4️⃣ SEO optimization...")
        seo_data = pipeline.seo_agent.optimize_seo(keyword_data)
        print("   ✅ SEO optimized")
        
        # Get the final content
        final_content = seo_data['final_content']
        
        print(f"🔍 About to post content:")
        print(f"   Length: {len(final_content)} characters")
        print(f"   Content: '{final_content}'")
        
        # Ensure content is under 280 characters for a single tweet
        if len(final_content) > 280:
            print(f"⚠️ Content is {len(final_content)} characters, which is over the 280 character limit for a single tweet.")
            # Take the first 277 characters and add "..." 
            truncated_content = final_content[:277] + "..."
            print(f"   Truncating to: '{truncated_content}'")
            response = pipeline.twitter_client.post_tweet(truncated_content)
        else:
            # Post the tweet
            response = pipeline.twitter_client.post_tweet(final_content)
        
        if response:
            tweet_data = {
                'tweet_id': str(response.data['id']),
                'content': final_content,
                'content_type': daily_plan['type'],
                'theme': research_data.get('theme'),
                'posted_at': datetime.now(),
                'attempts_needed': 1
            }
            pipeline.db.save_tweet_analytics(tweet_data)
            
            print(f"🎉 Manual tweet posted successfully!")
            print(f"   📊 Tweet ID: {response.data['id']}")
            print(f"   📝 Content Type: {daily_plan['type']}")
            print(f"   🎯 Theme: {research_data.get('theme')}")
            return True
        else:
            print("❌ Failed to post tweet")
            return False
            
    except Exception as e:
        print(f"❌ Error in manual posting: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    manual_post()
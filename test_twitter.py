#!/usr/bin/env python3
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

def test_twitter_api():
    """Test Twitter API credentials and permissions"""
    print("Testing Twitter API credentials...")
    
    try:
        # Test with v2 API
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        
        # Test getting user info
        me = client.get_me()
        if me.data:
            print(f"✅ Successfully authenticated as: @{me.data.username} (ID: {me.data.id})")
        else:
            print("❌ Failed to get user info")
            return False
            
        # Test posting a simple tweet
        test_content = "Testing Twitter API connection - this is an automated test tweet. Please ignore. #Test"
        print(f"Attempting to post test tweet: '{test_content}'")
        response = client.create_tweet(text=test_content)
        
        if response.data:
            tweet_id = response.data['id']
            print(f"✅ Successfully posted test tweet with ID: {tweet_id}")
            
            # Try to delete the test tweet
            try:
                client.delete_tweet(tweet_id)
                print("✅ Successfully deleted test tweet")
            except Exception as e:
                print(f"⚠️ Could not delete test tweet (not critical): {e}")
            
            return True
        else:
            print("❌ Failed to post test tweet")
            return False
            
    except Exception as e:
        print(f"❌ Twitter API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_twitter_api()
    if success:
        print("\n🎉 All Twitter API tests passed!")
    else:
        print("\n❌ Twitter API tests failed. Please check your credentials and permissions.")
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Twitter API credentials...")

# Initialize Twitter client
try:
    client = tweepy.Client(
        bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        wait_on_rate_limit=True
    )
    print("✅ Twitter client initialized")
    
    # Test authentication by getting user info
    me = client.get_me()
    print(f"✅ Authenticated as: @{me.data.username}")
    
    # Test posting capability
    test_tweet = "Testing AI automation system - please ignore this test tweet!"
    response = client.create_tweet(text=test_tweet)
    print(f"✅ Test tweet posted successfully!")
    print(f"   Tweet ID: {response.data['id']}")
    
except tweepy.Forbidden as e:
    print(f"❌ 403 Forbidden Error: {e}")
    print("   This usually means:")
    print("   - App permissions need to be activated")
    print("   - Account needs verification")
    print("   - API keys need regeneration")
    
except tweepy.Unauthorized as e:
    print(f"❌ 401 Unauthorized Error: {e}")
    print("   This usually means invalid API keys")
    
except Exception as e:
    print(f"❌ Other Error: {e}")
    print(f"   Error type: {type(e)}")


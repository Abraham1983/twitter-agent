# Add this debug function to your main.py temporarily
def debug_twitter_post(self, content):
    print(f"🔍 DEBUG: Content to post:")
    print(f"   Length: {len(content)} characters")
    print(f"   Content: '{content}'")
    print(f"   Type: {type(content)}")
    
    # Test with the exact same client setup that worked
    import tweepy
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    client = tweepy.Client(
        bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        wait_on_rate_limit=True
    )
    
    try:
        response = client.create_tweet(text=content)
        print(f"✅ DEBUG: Direct post successful: {response.data['id']}")
        return response
    except Exception as e:
        print(f"❌ DEBUG: Direct post failed: {e}")
        return None

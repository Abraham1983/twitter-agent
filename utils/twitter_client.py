import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterClient:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
    
    def post_tweet(self, content):
        try:
            response = self.client.create_tweet(text=content)
            print(f"✅ Tweet posted successfully: {response}")
            return response
        except Exception as e:
            print(f"❌ Error posting tweet: {e}")
            return None
    
    def reply_to_tweet(self, content, reply_to_id):
        try:
            response = self.client.create_tweet(
                text=content, 
                in_reply_to_tweet_id=reply_to_id
            )
            print(f"✅ Reply posted successfully")
            return response
        except Exception as e:
            print(f"❌ Error posting reply: {e}")
            return None
    
    def get_my_user_id(self):
        """Get the authenticated user's ID"""
        try:
            me = self.client.get_me()
            return me.data.id
        except Exception as e:
            print(f"❌ Error getting user ID: {e}")
            return None
    
    def get_users_mentions(self, user_id, since_id=None, max_results=10):
        """Get mentions of the authenticated user"""
        try:
            mentions = self.client.get_users_mentions(
                id=user_id,
                since_id=since_id,
                max_results=max_results,
                tweet_fields=["created_at", "author_id", "conversation_id", "in_reply_to_user_id"]
            )
            return mentions
        except Exception as e:
            print(f"❌ Error getting user mentions: {e}")
            return None
    
    def get_tweet_replies(self, conversation_id, max_results=100):
        """Get replies to a specific tweet using conversation_id"""
        try:
            # Search for all tweets in the same conversation
            query = f"conversation_id:{conversation_id}"
            replies = self.client.search_recent_tweets(
                query=query,
                tweet_fields=["created_at", "author_id", "in_reply_to_user_id", "referenced_tweets"],
                max_results=max_results
            )
            return replies
        except Exception as e:
            print(f"❌ Error getting tweet replies: {e}")
            return None
    
    def get_conversation_thread(self, tweet_id):
        """Get the complete conversation thread for a tweet"""
        try:
            # First get the original tweet to retrieve conversation_id
            tweet = self.client.get_tweet(
                id=tweet_id,
                tweet_fields=["conversation_id"]
            )
            
            if not tweet.data:
                print(f"❌ Could not retrieve tweet with ID: {tweet_id}")
                return None
                
            conversation_id = tweet.data.conversation_id
            
            # Get all tweets in the conversation
            query = f"conversation_id:{conversation_id}"
            conversation = self.client.search_recent_tweets(
                query=query,
                tweet_fields=["created_at", "author_id", "in_reply_to_user_id", "referenced_tweets", "text"],
                max_results=100
            )
            
            return conversation
        except Exception as e:
            print(f"❌ Error getting conversation thread: {e}")
            return None

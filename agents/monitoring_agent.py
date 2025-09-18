from utils.twitter_client import TwitterClient
from utils.database import TwitterDatabase
from agents.response_agent import ResponseAgent
import time
import os
import sqlite3
from datetime import datetime

class MonitoringAgent:
    def __init__(self):
        self.twitter_client = TwitterClient()
        self.db = TwitterDatabase()
        self.response_agent = ResponseAgent()
        self.last_mention_id = None
        self.my_user_id = None
        
    def initialize_agent(self):
        """Initialize the monitoring agent by getting user ID"""
        self.my_user_id = self.twitter_client.get_my_user_id()
        if self.my_user_id:
            print(f"✅ Monitoring agent initialized for user ID: {self.my_user_id}")
            return True
        else:
            print("❌ Failed to initialize monitoring agent")
            return False
    
    def monitor_mentions(self, max_results=10):
        """Monitor new mentions of the authenticated user"""
        if not self.my_user_id:
            print("❌ Monitoring agent not initialized")
            return None
            
        try:
            mentions = self.twitter_client.get_users_mentions(
                user_id=self.my_user_id,
                since_id=self.last_mention_id,
                max_results=max_results
            )
            
            if mentions and mentions.data:
                # Update the last mention ID to the newest mention
                self.last_mention_id = mentions.data[0].id
                print(f"✅ Found {len(mentions.data)} new mentions")
                return mentions.data
            else:
                print("🔍 No new mentions found")
                return []
                
        except Exception as e:
            print(f"❌ Error monitoring mentions: {e}")
            return None
    
    def get_tweet_replies(self, tweet_id):
        """Get replies to a specific tweet"""
        try:
            # First get the original tweet to retrieve conversation_id
            tweet = self.twitter_client.client.get_tweet(
                id=tweet_id,
                tweet_fields=["conversation_id"]
            )
            
            if not tweet.data:
                print(f"❌ Could not retrieve tweet with ID: {tweet_id}")
                return None
                
            conversation_id = tweet.data.conversation_id
            
            # Get all tweets in the conversation
            replies = self.twitter_client.get_tweet_replies(conversation_id)
            
            if replies and replies.data:
                # Filter for direct replies to the original tweet
                direct_replies = []
                for reply in replies.data:
                    # Check if this tweet is a reply to our original tweet
                    if (hasattr(reply, 'referenced_tweets') and reply.referenced_tweets):
                        for ref_tweet in reply.referenced_tweets:
                            if ref_tweet.id == tweet_id and ref_tweet.type == 'replied_to':
                                direct_replies.append(reply)
                                break
                    elif hasattr(reply, 'in_reply_to_user_id') and reply.in_reply_to_user_id == self.my_user_id:
                        direct_replies.append(reply)
                
                print(f"✅ Found {len(direct_replies)} direct replies to tweet {tweet_id}")
                return direct_replies
            else:
                print(f"🔍 No replies found for tweet {tweet_id}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting replies for tweet {tweet_id}: {e}")
            return None
    
    def get_conversation_thread(self, tweet_id):
        """Get the complete conversation thread for a tweet"""
        try:
            conversation = self.twitter_client.get_conversation_thread(tweet_id)
            
            if conversation and conversation.data:
                print(f"✅ Retrieved conversation thread with {len(conversation.data)} tweets")
                return conversation.data
            else:
                print(f"🔍 No conversation data found for tweet {tweet_id}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting conversation thread for tweet {tweet_id}: {e}")
            return None
    
    def process_mentions(self, mentions):
        """Process mentions and store engagement data in database"""
        if not mentions:
            return
            
        for mention in mentions:
            try:
                # Store mention in database as engagement
                engagement_data = {
                    'tweet_id': str(mention.id),
                    'user_id': str(mention.author_id),
                    'username': f"User_{mention.author_id}",  # Would need to fetch actual username
                    'interaction_type': 'mention',
                    'content': mention.text,
                    'timestamp': mention.created_at,
                    'responded': False,
                    'lead_score': 0
                }
                
                # Save engagement data using the database method
                self.db.save_engagement_data(engagement_data)
                
                print(f"✅ Stored mention from user {mention.author_id}")
                
            except Exception as e:
                print(f"❌ Error processing mention {mention.id}: {e}")
    
    def respond_to_comments(self):
        """Respond to unresponded comments using the ResponseAgent"""
        try:
            # Get unresponded mentions from database
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tweet_id, user_id, username, content 
                FROM engagements 
                WHERE interaction_type = 'mention' AND responded = FALSE
                ORDER BY timestamp ASC
            """)
            
            unresponded_mentions = cursor.fetchall()
            conn.close()
            
            if not unresponded_mentions:
                print("🔍 No unresponded mentions found")
                return
            
            print(f"💬 Found {len(unresponded_mentions)} unresponded mentions")
            
            # Respond to each mention
            for mention_row in unresponded_mentions:
                tweet_id, user_id, username, content = mention_row
                
                # Get the original tweet content to provide context
                original_tweet = self.twitter_client.client.get_tweet(
                    id=tweet_id,
                    tweet_fields=["text"]
                )
                
                original_content = original_tweet.data.text if original_tweet and original_tweet.data else None
                
                # Prepare comment data for the response agent
                comment_data = {
                    'tweet_id': tweet_id,
                    'user_id': user_id,
                    'username': username,
                    'content': content
                }
                
                # Generate response using the ResponseAgent
                response_content = self.response_agent.generate_response(comment_data, original_content)
                
                if response_content:
                    # Post the response
                    reply_response = self.twitter_client.reply_to_tweet(response_content, tweet_id)
                    
                    if reply_response:
                        # Mark as responded in database
                        conn = sqlite3.connect(self.db.db_path)
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE engagements 
                            SET responded = TRUE 
                            WHERE tweet_id = ?
                        """, (tweet_id,))
                        conn.commit()
                        conn.close()
                        
                        print(f"✅ Successfully responded to mention from @{username}")
                    else:
                        print(f"❌ Failed to post response to @{username}")
                else:
                    print(f"❌ Failed to generate response for @{username}")
                    
        except Exception as e:
            print(f"❌ Error responding to comments: {e}")
    
    def monitor_new_engagements(self, interval_minutes=5):
        """Continuously monitor for new mentions and engagements"""
        print(f"🚀 Starting engagement monitoring (checking every {interval_minutes} minutes)")
        
        if not self.initialize_agent():
            return
            
        try:
            while True:
                print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking for new mentions...")
                
                # Monitor mentions
                mentions = self.monitor_mentions()
                
                if mentions and len(mentions) > 0:
                    print(f"🔔 New mentions detected: {len(mentions)}")
                    self.process_mentions(mentions)
                    
                    # For each mention, check for replies
                    for mention in mentions:
                        replies = self.get_tweet_replies(mention.id)
                        if replies and len(replies) > 0:
                            print(f"💬 Found {len(replies)} replies to mention {mention.id}")
                
                # Respond to comments
                self.respond_to_comments()
                
                # Wait before next check
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Error in monitoring loop: {e}")

if __name__ == "__main__":
    # Test the monitoring agent
    agent = MonitoringAgent()
    if agent.initialize_agent():
        # Run a single check for mentions
        mentions = agent.monitor_mentions()
        agent.process_mentions(mentions)
        # Respond to comments
        agent.respond_to_comments()
    else:
        print("❌ Failed to initialize monitoring agent")
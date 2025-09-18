from utils.twitter_client import TwitterClient
from agents.response_agent import ResponseAgent
import tweepy
import sqlite3
import random

class EngagementAgent:
    def __init__(self):
        self.twitter_client = TwitterClient()
        self.response_agent = ResponseAgent()
        self.client = self.twitter_client.client
    
    def find_target_audience_content(self, target_keywords, max_results=10):
        """
        Find content from target audience to engage with
        target_keywords: List of keywords that define your target audience
        """
        try:
            # Create a query combining target keywords
            query = " OR ".join(target_keywords) + " -is:retweet lang:en"
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "author_id", "public_metrics", "context_annotations"]
            )
            
            if not tweets.data:
                return {"target_keywords": target_keywords, "tweets": [], "total": 0}
            
            formatted_tweets = []
            for tweet in tweets.data:
                formatted_tweets.append({
                    "id": tweet.id,
                    "text": tweet.text,
                    "author_id": tweet.author_id,
                    "created_at": tweet.created_at,
                    "retweet_count": tweet.public_metrics['retweet_count'],
                    "like_count": tweet.public_metrics['like_count'],
                    "reply_count": tweet.public_metrics['reply_count']
                })
            
            return {
                "target_keywords": target_keywords,
                "tweets": formatted_tweets,
                "total": len(formatted_tweets)
            }
            
        except Exception as e:
            return {"error": f"Failed to find target audience content: {str(e)}"}
    
    def generate_engagement_response(self, tweet_data):
        """
        Generate a valuable response to engage with target audience content
        """
        try:
            # Prepare comment data for the response agent
            comment_data = {
                'tweet_id': tweet_data['id'],
                'user_id': tweet_data['author_id'],
                'username': f"user_{tweet_data['author_id']}",  # Would need to fetch actual username
                'content': tweet_data['text']
            }
            
            # Generate response using the ResponseAgent
            response_content = self.response_agent.generate_response(comment_data)
            
            return response_content
            
        except Exception as e:
            return None
    
    def engage_with_content(self, tweet_data, engagement_type="like_and_comment"):
        """
        Proactively engage with content from your target audience
        engagement_type: "like", "retweet", "comment", or "like_and_comment"
        """
        try:
            results = {
                "tweet_id": tweet_data['id'],
                "actions": []
            }
            
            # Like the tweet
            if engagement_type in ["like", "like_and_comment"]:
                try:
                    self.client.like(tweet_data['id'])
                    results["actions"].append("liked")
                except Exception as e:
                    results["actions"].append(f"like_failed: {str(e)}")
            
            # Retweet (be careful with this, might want to add more logic)
            if engagement_type == "retweet":
                try:
                    self.client.retweet(tweet_data['id'])
                    results["actions"].append("retweeted")
                except Exception as e:
                    results["actions"].append(f"retweet_failed: {str(e)}")
            
            # Comment on the tweet
            if engagement_type in ["comment", "like_and_comment"]:
                response_content = self.generate_engagement_response(tweet_data)
                if response_content:
                    try:
                        reply_response = self.twitter_client.reply_to_tweet(response_content, tweet_data['id'])
                        if reply_response:
                            results["actions"].append("commented")
                            results["comment"] = response_content
                        else:
                            results["actions"].append("comment_failed")
                    except Exception as e:
                        results["actions"].append(f"comment_failed: {str(e)}")
                else:
                    results["actions"].append("comment_generation_failed")
            
            return results
            
        except Exception as e:
            return {"error": f"Failed to engage with content: {str(e)}"}
    
    def get_user_profile(self, user_id):
        """
        Get information about a Twitter user
        """
        try:
            user = self.client.get_user(
                id=user_id,
                user_fields=["public_metrics", "description", "verified"]
            )
            
            if not user.data:
                return None
            
            return {
                "id": user.data.id,
                "username": user.data.username,
                "name": user.data.name,
                "followers_count": user.data.public_metrics['followers_count'],
                "following_count": user.data.public_metrics['following_count'],
                "tweet_count": user.data.public_metrics['tweet_count'],
                "verified": user.data.verified,
                "description": user.data.description
            }
            
        except Exception as e:
            return None
    
    def identify_influencers(self, niche_keywords, min_followers=10000):
        """
        Identify influencers in your niche based on keywords and follower count
        """
        try:
            # Find recent tweets with niche keywords
            query = " OR ".join(niche_keywords) + " lang:en"
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=50,
                tweet_fields=["author_id"]
            )
            
            if not tweets.data:
                return {"influencers": [], "total": 0}
            
            # Get unique author IDs
            author_ids = list(set([tweet.author_id for tweet in tweets.data]))
            
            # Get user profiles and filter for influencers
            influencers = []
            for author_id in author_ids[:20]:  # Limit to first 20 to avoid rate limits
                user_profile = self.get_user_profile(author_id)
                if user_profile and user_profile["followers_count"] >= min_followers:
                    influencers.append(user_profile)
            
            # Sort by followers count
            influencers.sort(key=lambda x: x["followers_count"], reverse=True)
            
            return {
                "influencers": influencers,
                "total": len(influencers)
            }
            
        except Exception as e:
            return {"error": f"Failed to identify influencers: {str(e)}"}
    
    def follow_target_users(self, user_ids, max_follows=10):
        """
        Follow users in your target audience (use carefully)
        """
        try:
            followed_users = []
            for user_id in user_ids[:max_follows]:
                try:
                    self.client.follow_user(user_id)
                    followed_users.append(user_id)
                except Exception as e:
                    # User might already be followed, or other issues
                    continue
            
            return {
                "followed_users": followed_users,
                "total_followed": len(followed_users)
            }
            
        except Exception as e:
            return {"error": f"Failed to follow users: {str(e)}"}
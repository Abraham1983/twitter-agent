from utils.twitter_client import TwitterClient
import tweepy

class TrendAnalysisAgent:
    def __init__(self):
        self.twitter_client = TwitterClient()
        self.client = self.twitter_client.client
    
    def get_trending_topics(self, woeid=1):  # 1 = Worldwide, 23424977 = United States
        """
        Get trending topics for a specific location
        woeid: Where On Earth ID for location (default: 1 = Worldwide)
        """
        try:
            trends_result = self.client.get_place_trends(id=woeid)
            
            if not trends_result.data:
                return {"error": "No trend data available"}
            
            trends = trends_result.data[0]['trends']
            
            # Filter out trends without tweet volumes
            trending_with_volume = [trend for trend in trends if trend['tweet_volume'] is not None]
            
            # Sort by tweet volume
            trending_with_volume.sort(key=lambda x: x['tweet_volume'] or 0, reverse=True)
            
            # Format the results
            formatted_trends = []
            for trend in trending_with_volume[:20]:  # Top 20 trends
                formatted_trends.append({
                    "name": trend['name'],
                    "url": trend['url'],
                    "tweet_volume": trend['tweet_volume'],
                    "promoted_content": trend['promoted_content']
                })
            
            return {
                "location_woeid": woeid,
                "trends": formatted_trends,
                "total_trends": len(formatted_trends)
            }
            
        except Exception as e:
            return {"error": f"Failed to get trending topics: {str(e)}"}
    
    def get_trending_hashtags(self, woeid=1):
        """
        Get only trending hashtags (topics starting with #)
        """
        trends_data = self.get_trending_topics(woeid)
        
        if "error" in trends_data:
            return trends_data
        
        hashtags = [trend for trend in trends_data["trends"] if trend["name"].startswith("#")]
        
        return {
            "location_woeid": woeid,
            "hashtags": hashtags,
            "total_hashtags": len(hashtags)
        }
    
    def get_trending_keywords(self, woeid=1, exclude_hashtags=True):
        """
        Get trending keywords (excluding hashtags if specified)
        """
        trends_data = self.get_trending_topics(woeid)
        
        if "error" in trends_data:
            return trends_data
        
        if exclude_hashtags:
            keywords = [trend for trend in trends_data["trends"] if not trend["name"].startswith("#")]
        else:
            keywords = trends_data["trends"]
        
        return {
            "location_woeid": woeid,
            "keywords": keywords,
            "total_keywords": len(keywords)
        }
    
    def search_trending_content(self, query, max_results=10):
        """
        Search for recent tweets about a trending topic
        """
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "author_id", "public_metrics"]
            )
            
            if not tweets.data:
                return {"query": query, "tweets": [], "total": 0}
            
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
                "query": query,
                "tweets": formatted_tweets,
                "total": len(formatted_tweets)
            }
            
        except Exception as e:
            return {"error": f"Failed to search trending content: {str(e)}"}
    
    def analyze_trend_relevance(self, trends, niche_keywords):
        """
        Analyze which trends are most relevant to your niche
        niche_keywords: List of keywords relevant to your niche
        """
        relevant_trends = []
        
        for trend in trends.get("trends", []):
            trend_name = trend["name"].lower()
            # Check if any niche keywords are in the trend name
            relevance_score = sum(1 for keyword in niche_keywords if keyword.lower() in trend_name)
            
            if relevance_score > 0:
                relevant_trends.append({
                    "trend": trend,
                    "relevance_score": relevance_score
                })
        
        # Sort by relevance score
        relevant_trends.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return {
            "relevant_trends": relevant_trends,
            "total_relevant": len(relevant_trends)
        }
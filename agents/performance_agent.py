from utils.database import TwitterDatabase
import sqlite3
from collections import defaultdict
import re

class PerformanceAgent:
    def __init__(self):
        self.db = TwitterDatabase()
    
    def analyze_performance(self):
        """
        Analyze past post metrics to identify patterns and optimize future content
        """
        try:
            # Get all tweet analytics data
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tweet_id, content, likes, retweets, replies, performance_score, posted_at
                FROM tweet_analytics
                ORDER BY posted_at DESC
            """)
            
            tweets = cursor.fetchall()
            conn.close()
            
            if not tweets:
                return {"message": "No tweet data available for analysis"}
            
            # Calculate basic statistics
            total_tweets = len(tweets)
            total_likes = sum(tweet[2] for tweet in tweets)
            total_retweets = sum(tweet[3] for tweet in tweets)
            total_replies = sum(tweet[4] for tweet in tweets)
            
            avg_likes = total_likes / total_tweets if total_tweets > 0 else 0
            avg_retweets = total_retweets / total_tweets if total_tweets > 0 else 0
            avg_replies = total_replies / total_tweets if total_tweets > 0 else 0
            
            # Analyze content patterns
            hashtag_performance = self._analyze_hashtags(tweets)
            content_type_performance = self._analyze_content_types(tweets)
            timing_performance = self._analyze_timing(tweets)
            
            # Identify top performing tweets
            top_tweets = sorted(tweets, key=lambda x: (x[2] + x[3] + x[4]), reverse=True)[:5]
            
            analysis = {
                "total_tweets_analyzed": total_tweets,
                "average_metrics": {
                    "likes": round(avg_likes, 2),
                    "retweets": round(avg_retweets, 2),
                    "replies": round(avg_replies, 2)
                },
                "top_performing_tweets": [
                    {
                        "tweet_id": tweet[0],
                        "content": tweet[1][:100] + "..." if len(tweet[1]) > 100 else tweet[1],
                        "likes": tweet[2],
                        "retweets": tweet[3],
                        "replies": tweet[4],
                        "total_engagement": tweet[2] + tweet[3] + tweet[4]
                    }
                    for tweet in top_tweets
                ],
                "hashtag_analysis": hashtag_performance,
                "content_type_analysis": content_type_performance,
                "timing_analysis": timing_performance
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"Performance analysis failed: {str(e)}"}
    
    def _analyze_hashtags(self, tweets):
        """Analyze performance based on hashtags used"""
        hashtag_stats = defaultdict(lambda: {"count": 0, "total_likes": 0, "total_retweets": 0, "total_replies": 0})
        
        for tweet in tweets:
            tweet_id, content, likes, retweets, replies, perf_score, posted_at = tweet
            # Extract hashtags
            hashtags = re.findall(r'#\w+', content)
            
            for hashtag in hashtags:
                hashtag_stats[hashtag]["count"] += 1
                hashtag_stats[hashtag]["total_likes"] += likes
                hashtag_stats[hashtag]["total_retweets"] += retweets
                hashtag_stats[hashtag]["total_replies"] += replies
        
        # Calculate averages
        hashtag_performance = {}
        for hashtag, stats in hashtag_stats.items():
            count = stats["count"]
            hashtag_performance[hashtag] = {
                "usage_count": count,
                "avg_likes": round(stats["total_likes"] / count, 2) if count > 0 else 0,
                "avg_retweets": round(stats["total_retweets"] / count, 2) if count > 0 else 0,
                "avg_replies": round(stats["total_replies"] / count, 2) if count > 0 else 0,
                "total_engagement": stats["total_likes"] + stats["total_retweets"] + stats["total_replies"]
            }
        
        # Sort by total engagement
        sorted_hashtags = sorted(hashtag_performance.items(), 
                               key=lambda x: x[1]["total_engagement"], reverse=True)
        
        return dict(sorted_hashtags[:10])  # Top 10 hashtags
    
    def _analyze_content_types(self, tweets):
        """Categorize and analyze performance by content type"""
        content_categories = {
            "technical": ["python", "automation", "ai", "machine learning", "cybersecurity", "docker", "kubernetes", "api"],
            "business": ["roi", "productivity", "efficiency", "client", "business", "startup", "entrepreneur"],
            "personal": ["journey", "experience", "career", "learning", "growth"],
            "tutorial": ["how to", "tutorial", "guide", "step by step", "learn"],
            "news": ["announc", "launch", "new", "update", "release"]
        }
        
        category_stats = defaultdict(lambda: {"count": 0, "total_likes": 0, "total_retweets": 0, "total_replies": 0})
        
        for tweet in tweets:
            tweet_id, content, likes, retweets, replies, perf_score, posted_at = tweet
            content_lower = content.lower()
            
            # Categorize tweet
            categorized = False
            for category, keywords in content_categories.items():
                if any(keyword in content_lower for keyword in keywords):
                    category_stats[category]["count"] += 1
                    category_stats[category]["total_likes"] += likes
                    category_stats[category]["total_retweets"] += retweets
                    category_stats[category]["total_replies"] += replies
                    categorized = True
            
            # If not categorized, put in "other"
            if not categorized:
                category_stats["other"]["count"] += 1
                category_stats["other"]["total_likes"] += likes
                category_stats["other"]["total_retweets"] += retweets
                category_stats["other"]["total_replies"] += replies
        
        # Calculate averages
        category_performance = {}
        for category, stats in category_stats.items():
            count = stats["count"]
            if count > 0:
                category_performance[category] = {
                    "tweet_count": count,
                    "avg_likes": round(stats["total_likes"] / count, 2),
                    "avg_retweets": round(stats["total_retweets"] / count, 2),
                    "avg_replies": round(stats["total_replies"] / count, 2),
                    "total_engagement": stats["total_likes"] + stats["total_retweets"] + stats["total_replies"]
                }
        
        # Sort by total engagement
        sorted_categories = sorted(category_performance.items(), 
                                 key=lambda x: x[1]["total_engagement"], reverse=True)
        
        return dict(sorted_categories)
    
    def _analyze_timing(self, tweets):
        """Analyze performance based on posting timing"""
        hour_stats = defaultdict(lambda: {"count": 0, "total_engagement": 0})
        
        for tweet in tweets:
            tweet_id, content, likes, retweets, replies, perf_score, posted_at = tweet
            # Extract hour from timestamp (assuming it's in a parseable format)
            try:
                from datetime import datetime
                if isinstance(posted_at, str):
                    dt = datetime.fromisoformat(posted_at.replace('Z', '+00:00'))
                else:
                    dt = posted_at
                
                hour = dt.hour
                engagement = likes + retweets + replies
                
                hour_stats[hour]["count"] += 1
                hour_stats[hour]["total_engagement"] += engagement
            except Exception as e:
                continue  # Skip if timestamp parsing fails
        
        # Calculate averages
        timing_performance = {}
        for hour, stats in hour_stats.items():
            count = stats["count"]
            if count > 0:
                timing_performance[f"{hour:02d}:00"] = {
                    "post_count": count,
                    "avg_engagement": round(stats["total_engagement"] / count, 2),
                    "total_engagement": stats["total_engagement"]
                }
        
        # Sort by average engagement
        sorted_timing = sorted(timing_performance.items(), 
                             key=lambda x: x[1]["avg_engagement"], reverse=True)
        
        return dict(sorted_timing)
    
    def get_content_recommendations(self):
        """Provide recommendations for future content based on performance analysis"""
        analysis = self.analyze_performance()
        
        if "error" in analysis:
            return analysis
        
        recommendations = {
            "best_hashtags": [],
            "best_content_types": [],
            "optimal_posting_times": [],
            "content_strategy": []
        }
        
        # Hashtag recommendations
        if "hashtag_analysis" in analysis:
            top_hashtags = sorted(analysis["hashtag_analysis"].items(), 
                                key=lambda x: x[1]["total_engagement"], reverse=True)[:5]
            recommendations["best_hashtags"] = [hashtag for hashtag, _ in top_hashtags]
        
        # Content type recommendations
        if "content_type_analysis" in analysis:
            top_content_types = sorted(analysis["content_type_analysis"].items(), 
                                     key=lambda x: x[1]["total_engagement"], reverse=True)[:3]
            recommendations["best_content_types"] = [ctype for ctype, _ in top_content_types]
        
        # Timing recommendations
        if "timing_analysis" in analysis:
            top_times = sorted(analysis["timing_analysis"].items(), 
                             key=lambda x: x[1]["avg_engagement"], reverse=True)[:3]
            recommendations["optimal_posting_times"] = [time for time, _ in top_times]
        
        # Content strategy recommendations
        avg_likes = analysis["average_metrics"]["likes"]
        avg_retweets = analysis["average_metrics"]["retweets"]
        avg_replies = analysis["average_metrics"]["replies"]
        
        recommendations["content_strategy"] = [
            f"Focus on content that drives engagement (current avg: {avg_likes + avg_retweets + avg_replies:.1f} total engagement per post)",
            f"Use top performing hashtags: {', '.join(recommendations['best_hashtags'][:3])}",
            f"Emphasize content types like: {', '.join(recommendations['best_content_types'])}",
            f"Post during peak hours: {', '.join(recommendations['optimal_posting_times'])}"
        ]
        
        return recommendations
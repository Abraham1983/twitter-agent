import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class TwitterDatabase:
    def __init__(self, db_path="data/twitter_data.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweet_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT UNIQUE,
                content TEXT,
                posted_at TIMESTAMP,
                likes INTEGER DEFAULT 0,
                retweets INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                performance_score REAL DEFAULT 0,
                last_updated TIMESTAMP
            )
        """)
        
        # Engagement table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS engagements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT,
                user_id TEXT,
                username TEXT,
                interaction_type TEXT,
                content TEXT,
                timestamp TIMESTAMP,
                responded BOOLEAN DEFAULT FALSE,
                lead_score INTEGER DEFAULT 0
            )
        """)
        
        # Trend analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trend_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                woeid INTEGER,
                location_name TEXT,
                trend_name TEXT,
                tweet_volume INTEGER,
                promoted_content BOOLEAN,
                analysis_type TEXT,
                relevance_score REAL DEFAULT 0
            )
        """)
        
        # Performance analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                analysis_type TEXT,
                category TEXT,
                metric_name TEXT,
                value REAL,
                sample_size INTEGER,
                recommendation TEXT
            )
        """)
        
        # Proactive engagement table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proactive_engagement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                target_tweet_id TEXT,
                target_user_id TEXT,
                action_taken TEXT,
                response_content TEXT,
                success BOOLEAN,
                engagement_metrics JSON
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_tweet_analytics(self, tweet_data: Dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO tweet_analytics 
            (tweet_id, content, posted_at, likes, retweets, replies, performance_score, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tweet_data.get('tweet_id'),
            tweet_data.get('content'),
            tweet_data.get('posted_at'),
            tweet_data.get('likes', 0),
            tweet_data.get('retweets', 0),
            tweet_data.get('replies', 0),
            tweet_data.get('performance_score', 0),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def save_engagement_data(self, engagement_data: Dict):
        """Save engagement data to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO engagements 
            (tweet_id, user_id, username, interaction_type, content, timestamp, responded, lead_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            engagement_data.get('tweet_id'),
            engagement_data.get('user_id'),
            engagement_data.get('username'),
            engagement_data.get('interaction_type'),
            engagement_data.get('content'),
            engagement_data.get('timestamp'),
            engagement_data.get('responded', False),
            engagement_data.get('lead_score', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def save_trend_analysis(self, trend_data: Dict):
        """Save trend analysis data to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save each trend
        for trend in trend_data.get('trends', []):
            cursor.execute("""
                INSERT INTO trend_analysis 
                (woeid, location_name, trend_name, tweet_volume, promoted_content, analysis_type, relevance_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                trend_data.get('location_woeid'),
                trend_data.get('location_name', 'Unknown'),
                trend.get('name'),
                trend.get('tweet_volume'),
                trend.get('promoted_content', False),
                trend_data.get('analysis_type', 'topic'),
                trend.get('relevance_score', 0)
            ))
        
        conn.commit()
        conn.close()
    
    def save_performance_analysis(self, performance_data: Dict):
        """Save performance analysis data to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save hashtag performance data
        if 'hashtag_analysis' in performance_data:
            for hashtag, metrics in performance_data['hashtag_analysis'].items():
                cursor.execute("""
                    INSERT INTO performance_analysis 
                    (analysis_type, category, metric_name, value, sample_size, recommendation)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    'hashtag',
                    hashtag,
                    'avg_engagement',
                    metrics.get('avg_likes', 0) + metrics.get('avg_retweets', 0) + metrics.get('avg_replies', 0),
                    metrics.get('usage_count', 0),
                    f"Hashtag {hashtag} performs well with {metrics.get('usage_count', 0)} uses"
                ))
        
        # Save content type performance data
        if 'content_type_analysis' in performance_data:
            for content_type, metrics in performance_data['content_type_analysis'].items():
                cursor.execute("""
                    INSERT INTO performance_analysis 
                    (analysis_type, category, metric_name, value, sample_size, recommendation)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    'content_type',
                    content_type,
                    'avg_engagement',
                    metrics.get('avg_likes', 0) + metrics.get('avg_retweets', 0) + metrics.get('avg_replies', 0),
                    metrics.get('tweet_count', 0),
                    f"Content type '{content_type}' performs well with {metrics.get('tweet_count', 0)} posts"
                ))
        
        # Save timing performance data
        if 'timing_analysis' in performance_data:
            for time_slot, metrics in performance_data['timing_analysis'].items():
                cursor.execute("""
                    INSERT INTO performance_analysis 
                    (analysis_type, category, metric_name, value, sample_size, recommendation)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    'timing',
                    time_slot,
                    'avg_engagement',
                    metrics.get('avg_engagement', 0),
                    metrics.get('post_count', 0),
                    f"Posting at {time_slot} performs well with {metrics.get('post_count', 0)} posts"
                ))
        
        conn.commit()
        conn.close()
    
    def save_proactive_engagement(self, engagement_data: Dict):
        """Save proactive engagement data to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO proactive_engagement 
            (target_tweet_id, target_user_id, action_taken, response_content, success, engagement_metrics)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            engagement_data.get('target_tweet_id'),
            engagement_data.get('target_user_id'),
            engagement_data.get('action_taken'),
            engagement_data.get('response_content'),
            engagement_data.get('success', False),
            json.dumps(engagement_data.get('engagement_metrics', {}))
        ))
        
        conn.commit()
        conn.close()

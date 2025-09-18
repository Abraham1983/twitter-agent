# Twitter Engagement Monitoring

This module provides functionality to monitor Twitter mentions, replies, and conversation threads for the authenticated user.

## Features

1. **Mention Monitoring**: Track when your account is mentioned in tweets
2. **Reply Tracking**: Monitor replies to your tweets
3. **Conversation Threads**: Retrieve complete conversation threads
4. **Engagement Database**: Store engagement data for analysis

## Components

### 1. TwitterClient Extensions
The `utils/twitter_client.py` file has been extended with new methods:
- `get_my_user_id()`: Get the authenticated user's ID
- `get_users_mentions()`: Get mentions of the authenticated user
- `get_tweet_replies()`: Get replies to a specific tweet using conversation_id
- `get_conversation_thread()`: Get the complete conversation thread for a tweet

### 2. Monitoring Agent
The `agents/monitoring_agent.py` provides a dedicated agent for monitoring:
- Continuous monitoring of mentions
- Processing and storage of engagement data
- Reply and conversation thread retrieval

### 3. Monitoring Scheduler
The `monitor_scheduler.py` runs as a separate service to regularly check for new engagements.

## Usage

### Manual Monitoring
```python
from agents.monitoring_agent import MonitoringAgent

monitor = MonitoringAgent()
if monitor.initialize_agent():
    # Check for new mentions
    mentions = monitor.monitor_mentions()
    monitor.process_mentions(mentions)
```

### Continuous Monitoring
Run the monitoring scheduler:
```bash
python monitor_scheduler.py
```

### Database Storage
Engagement data is automatically stored in the SQLite database in the `engagements` table with the following fields:
- `tweet_id`: The ID of the tweet
- `user_id`: The ID of the user who engaged
- `username`: The username of the user who engaged
- `interaction_type`: Type of interaction (mention, reply, etc.)
- `content`: Content of the tweet
- `timestamp`: When the engagement occurred
- `responded`: Whether the engagement has been responded to
- `lead_score`: A score indicating the value of the engagement

## API Methods

### get_users_mentions()
```python
mentions = client.get_users_mentions(user_id, since_id=None, max_results=10)
```
Returns Tweets mentioning a single user specified by the requested user ID.

### get_tweet_replies()
```python
replies = client.get_tweet_replies(conversation_id, max_results=100)
```
Returns replies to a specific tweet using its conversation ID.

### get_conversation_thread()
```python
conversation = client.get_conversation_thread(tweet_id)
```
Returns the complete conversation thread for a tweet.

## Best Practices

1. **Rate Limiting**: The client is configured with `wait_on_rate_limit=True` to automatically handle rate limits
2. **Pagination**: Use `since_id` parameter to only retrieve new mentions since your last check
3. **Error Handling**: All methods include proper exception handling
4. **Data Storage**: Engagement data is stored to avoid duplicate processing
5. **Regular Monitoring**: Use the scheduler to check for new engagements regularly

## Setup

Ensure you have the required environment variables in your `.env` file:
- `TWITTER_BEARER_TOKEN`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
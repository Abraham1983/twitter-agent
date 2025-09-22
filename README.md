# Twitter Agent Pipeline

An AI-powered Twitter automation system that creates and posts strategic content while monitoring and engaging with your audience.

## Features

### 🤖 AI-Powered Content Creation
- **Research Agent**: Gathers information on topics using OpenRouter API
- **Writer Agent**: Creates engaging Twitter content using proven templates
- **Keyword Agent**: Optimizes content with relevant keywords
- **SEO Agent**: Enhances content discoverability
- **Boss Agent**: Reviews and approves content using Claude Sonnet 3.5

### 🔍 Trend Analysis & Performance Optimization
- **Trend Analysis Agent**: Monitors real-time trending topics and hashtags
- **Performance Agent**: Analyzes past post metrics to optimize future content
- **Engagement Agent**: Proactively engages with your target audience's content

### 📈 Monitoring & Engagement
- **Monitoring Agent**: Tracks mentions, replies, and conversation threads
- **Response Agent**: Generates authentic responses to comments using your personal persona
- **Content Calendar**: Strategic scheduling of posts (thread days, topic planning)

### 🛠 Technical Features
- SQLite database for analytics and engagement tracking
- Rate-limit compliant Twitter API integration
- Automated scheduling system
- Personal persona-based authentic engagement
- **Autonomous monitoring and self-healing system**

## System Architecture

```
Twitter Agent Pipeline
├── Content Creation Agents
│   ├── Research Agent
│   ├── Writer Agent
│   ├── Keyword Agent
│   ├── SEO Agent
│   └── Boss Agent (Approval)
├── Analytics & Optimization
│   ├── Trend Analysis Agent
│   ├── Performance Agent
│   └── Engagement Agent
├── Monitoring & Response
│   ├── Monitoring Agent
│   └── Response Agent
├── Autonomous Monitoring & Self-Healing
│   ├── Health Checks
│   ├── Failure Detection
│   ├── Recovery Mechanisms
│   └── Automated Fixes
├── Utilities
│   ├── Twitter Client
│   ├── Database
│   └── Content Calendar
└── Schedulers
    ├── Main Scheduler (Content posting)
    └── Monitoring Scheduler (Engagement tracking)
```

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Abraham1983/twitter-agent.git
   cd twitter-agent
   ```

2. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file with your API keys:
   ```env
   # Twitter API credentials
   TWITTER_BEARER_TOKEN=your_bearer_token
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

   # OpenRouter API key
   OPENROUTER_API_KEY=your_openrouter_key

   # Model settings
   SONNET_MODEL=anthropic/claude-3.5-sonnet
   HAIKU_MODEL=anthropic/claude-3-haiku
   ```

4. **Configure personal persona**:
   Update `config/personal_persona.py` with your authentic background and expertise.

5. **Initialize the database**:
   ```bash
   python3 main.py
   ```

6. **Run the scheduler**:
   ```bash
   python3 scheduler.py
   ```

## 📅 Scheduled Tasks

The system automatically runs these tasks:

- **9:00 AM & 3:00 PM**: Content posting
- **8:00 AM & 2:00 PM**: Pre-posting health checks (1 hour before content posting)
- **Every 2 hours**: Trend analysis
- **11:00 PM**: Performance analysis
- **Every 4 hours**: Proactive audience engagement
- **Every 30 minutes**: Comment responses
- **Every 15 minutes**: Engagement monitoring
- **Every 30 minutes**: Posting pipeline monitoring

## 🛠 Setup as System Service

1. Make scripts executable:
   ```bash
   chmod +x scheduler.py
   chmod +x setup_scheduler.sh
   chmod +x autonomous_monitor.py
   chmod +x setup_autonomous_monitor.sh
   ```

2. Run setup (requires sudo):
   ```bash
   sudo ./setup_scheduler.sh
   sudo ./setup_autonomous_monitor.sh
   ```

## 📊 Database Structure

The system uses SQLite with these tables:
- `tweet_analytics`: Post performance metrics
- `engagements`: Audience interactions
- `trend_analysis`: Trending topic data
- `performance_analysis`: Content performance insights
- `proactive_engagement`: Target audience engagement records

## 🎯 Content Strategy

The system uses a strategic content calendar that includes:
- Thread days for in-depth topics
- Educational explainers
- Technical tutorials
- Industry insights
- Personal journey updates

## 🔒 Security & Privacy

- API keys stored in `.env` file (excluded from Git)
- Rate-limit compliant API usage
- Secure credential handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For support, contact Abraham Vasquez at @AbrahamAv9728 on Twitter.
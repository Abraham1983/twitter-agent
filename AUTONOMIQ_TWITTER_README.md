# AutonomIQ Twitter Content Automation System

This system automatically generates and posts Twitter content for AutonomIQ based on your 12-month growth strategy.

## Daily Workflow

1. **Update your daily focus** (optional but recommended):
   ```bash
   ./update_daily_reminder.py
   ```

2. **Generate and post daily content**:
   ```bash
   ./daily_tweet_generator.py
   ```

## How It Works

The system follows your 12-month content strategy with 30-day cycles, posting 1-2 tweets per day covering:
- Personal journey updates about building AutonomIQ
- Educational content about AI automation for small businesses
- Hot takes and opinions on the AI industry
- Visual frameworks and diagrams
- Engagement boosters (polls, questions, memes)

## Content Types

- **Personal Journey**: Documenting the real experience of building AutonomIQ
- **Education Explainers**: Breaking down AI automation concepts for small businesses
- **Hot Takes**: Contrarian opinions on AI and automation trends
- **Visual Frameworks**: Diagrams and charts explaining AutonomIQ's approach
- **Engagement Boosters**: Polls, questions, and interactive content
- **Experiment Case Studies**: Real results from testing automation solutions

## Customization

- Content calendar in `utils/content_calendar.py`
- Persona details in `config/personal_persona.py`
- Daily reminders in `data/daily_reminder.json`

## Troubleshooting

If tweets fail to post, check:
- Twitter API credentials in `.env` file
- Content length (must be under 280 characters)
- Internet connectivity
- Error logs in `system_output.log`
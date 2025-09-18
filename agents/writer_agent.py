from utils.openrouter_client import OpenRouterClient
import os

class WriterAgent:
    def __init__(self):
        # Load authentic personal persona
        self.load_persona()
        
        self.client = OpenRouterClient()
        self.model = os.getenv('HAIKU_MODEL', 'anthropic/claude-3-haiku')

        # Your proven tweet templates
        self.templates = {
            "education_explainer": """
            Template: "Everyone talks about [topic] but here's the simple breakdown: 🧵👇"

            Thread structure:
            1. Hook tweet with thread indicator
            2. What it is (plain English)
            3. Why it matters for businesses
            4. Example use case
            5. Key takeaways
            6. Engagement closer: "What would you build with this?"

            Keep each tweet under 280 characters.
            """,

            "experiment_case_study": """
            Template: "Tried building [automation] today. Here's what worked ✅ ... and what instantly broke ❌"

            Structure:
            - Setup (what you tried)
            - 2-3 bullet wins
            - 2-3 failures
            - Lesson learned
            - End with: "Anyone else tested this?"

            Make it relatable and authentic.
            """,

            "hot_take_opinion": """
            Template: "Most people think [common belief]. They're wrong. Here's why: 👇"

            Structure:
            - Bold contrarian statement
            - Supporting evidence
            - Future prediction
            - End with: "Agree?"

            Be confident but not arrogant.
            """,

            "visual_framework": """
            Template: "Stop overcomplicating [topic]. Here's the simple framework I use 👇"

            Structure:
            - Problem statement
            - Framework description
            - Note about visual (will be added)
            - End with: "Should I turn this into a full thread?"

            Mention the visual component.
            """,

            "engagement_booster": """
            Template: Question or poll that sparks discussion

            Structure:
            - Interesting question about AI automation
            - Poll options (A/B/C/D) OR open question
            - Context if needed
            - End with: "Drop your thoughts 👇"

            Make it conversation-worthy.
            """,

            "personal_journey": """
            Template: "Documenting my AI journey publicly. Current status: [update]. Let's see where this goes 🚀"

            Structure:
            - Personal update
            - Small win or failure
            - What you learned
            - Future goal or next step

            Be authentic and relatable.
            """
        }

    def create_content(self, research_data):
        content_type = research_data.get('content_type', 'education_explainer')
        template = self.templates.get(content_type, self.templates['education_explainer'])

        messages = [
            {
                "role": "system",
                "content": f"""You are writing Twitter content for Abraham Vasquez (@AbrahamAv9728), AI Platform Engineer at Autonomiq.

AUTHENTIC BACKGROUND:
- 42-year-old AI Platform Engineer with 15+ years tech experience  
- Real achievements: 552% ROI, 99.8% efficiency improvements
- Previous roles: Tesla Process Engineer, Quest Diagnostics specialist
- Current projects: Azure SOC implementation, AWS honeypots, AI agents
- Seventh-day Adventist Christian, conservative values
- Pursuing cybersecurity certifications (CompTIA Security+, CISSP, etc.)

VOICE: Professional, mature, faith-informed, results-driven

                Brand voice:
                - Authoritative but approachable
                - Practical and results-focused
                - Helpful, not salesy
                - Technical but understandable

                Use this proven template:
                {template}

                Rules:
                - Keep tweets under 280 characters
                - Use 🧵👇 for threads
                - Maximum 1 emoji per tweet
                - Always end with engagement hook
                - Focus on business automation value
                - Be authentic and relatable
                """
            },
            {
                "role": "user",
                "content": f"""
                Content type: {content_type}
                Theme: {research_data.get('theme', 'general')}
                Research: {research_data['research']}

                Create engaging Twitter content that:
                1. Follows the template structure exactly
                2. Teaches something valuable about AI automation
                3. Attracts potential business clients
                4. Encourages genuine engagement
                5. Positions Abraham as a helpful automation expert with real credentials

                If it's an education_explainer, create a thread starting with the hook tweet.
                For other types, create a single engaging tweet.

                Make it sound natural and conversational, not robotic.
                Reference Abraham's actual experience and achievements when relevant.
                """
            }
        ]

        content = self.client.chat_completion(messages, self.model)

        return {
            "content": content,
            "content_type": content_type,
            "theme": research_data.get('theme'),
            "template_used": template,
            "research_used": research_data,
            "agent": "writer"
        }

    def create_content_with_feedback(self, research_data, boss_feedback):
        """Create revised content based on boss feedback"""
        
        content_type = research_data.get('content_type', 'education_explainer')
        template = self.templates.get(content_type, self.templates['education_explainer'])

        messages = [
            {
                "role": "system",
                "content": f"""You are revising Twitter content for Abraham Vasquez (@AbrahamAv9728), AI Platform Engineer at Autonomiq, based on CEO feedback.

                PREVIOUS VERSION WAS REJECTED. Address these CEO concerns:
                {boss_feedback}

                AUTHENTIC BACKGROUND:
                - 42-year-old AI Platform Engineer with 15+ years tech experience  
                - Real achievements: 552% ROI, 99.8% efficiency improvements
                - Previous roles: Tesla Process Engineer, Quest Diagnostics specialist
                - Current projects: Azure SOC implementation, AWS honeypots, AI agents
                - Seventh-day Adventist Christian, conservative values
                - Pursuing cybersecurity certifications (CompTIA Security+, CISSP, etc.)

                Brand voice:
                - Authoritative but approachable
                - Practical and results-focused
                - Helpful, not salesy
                - Technical but understandable

                Use this proven template:
                {template}

                REVISION REQUIREMENTS:
                1. Include specific metrics and numbers (Abraham's real achievements)
                2. Add professional credibility markers from actual background
                3. Include concrete examples with measurable outcomes
                4. Add clear business value proposition
                5. Include professional call-to-action

                Rules:
                - Keep tweets under 280 characters
                - Use 🧵👇 for threads
                - Maximum 1 emoji per tweet
                - Always end with engagement hook
                - Focus on business automation value
                - Be authentic and relatable
                """
            },
            {
                "role": "user",
                "content": f"""
                Content type: {content_type}
                Theme: {research_data.get('theme', 'general')}
                Research: {research_data['research']}

                SPECIFIC REVISIONS NEEDED (from CEO feedback):
                - Add concrete metrics and specific results (use Abraham's real 552% ROI, 99.8% improvements)
                - Include professional credibility indicators (Tesla, Autonomiq experience)
                - Provide unique insights that differentiate from competitors
                - Add clear value proposition for small businesses
                - Include strong call-to-action

                Create engaging Twitter content that:
                1. Follows the template structure exactly
                2. Addresses ALL CEO feedback points
                3. Uses Abraham's real metrics and achievements
                4. Demonstrates expertise with concrete examples
                5. Attracts potential business clients with clear value
                6. Encourages genuine engagement
                7. Positions Abraham as a results-driven automation expert

                Make it sound natural and conversational, not robotic.
                Focus on Abraham's specific, measurable business outcomes.
                """
            }
        ]

        content = self.client.chat_completion(messages, self.model)

        return {
            "content": content,
            "content_type": content_type,
            "theme": research_data.get('theme'),
            "template_used": template,
            "research_used": research_data,
            "boss_feedback_addressed": boss_feedback,
            "revision": True,
            "agent": "writer"
        }

    def load_persona(self):
        """Load authentic personal persona"""
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
        try:
            from personal_persona import PERSONAL_PERSONA, AUTHENTIC_PHRASES
            self.persona = PERSONAL_PERSONA
            self.authentic_phrases = AUTHENTIC_PHRASES
        except ImportError:
            self.persona = {}
            self.authentic_phrases = []

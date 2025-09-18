from utils.openrouter_client import OpenRouterClient
import os
import re

class BossAgent:
    def __init__(self):
        # Load authentic personal persona
        self.load_persona()
        
        self.client = OpenRouterClient()
        self.model = os.getenv('SONNET_MODEL', 'anthropic/claude-3.5-sonnet')

    def review_and_approve(self, research_data, writer_data, keyword_data, seo_data, attempt_number=1):
        messages = [
            {
                "role": "system",
                "content": f"""You are the CEO reviewing content before publication. This is attempt {attempt_number}.

                You have high standards for:
                1. Content quality and accuracy
                2. Brand consistency for an AI automation consultant
                3. Business value and client attraction
                4. Professional presentation with specific metrics
                5. Authority positioning and credibility markers

                Respond with either APPROVE or REJECT.

                If APPROVE: Start with "APPROVE:" then provide ONLY the final clean tweet content ready to post (no additional commentary).
                If REJECT: Start with "REJECT:" then provide specific, actionable feedback for improvement."""
            },
            {
                "role": "user",
                "content": f"""
                Review this content pipeline for an AI automation business:

                ATTEMPT: {attempt_number}
                RESEARCH THEME: {research_data.get('theme', 'general')}
                CONTENT TYPE: {research_data.get('content_type', 'general')}
                FINAL CONTENT: {seo_data['final_content']}

                This content should:
                - Attract small business owners who need automation services
                - Demonstrate expertise and authority
                - Include specific metrics and concrete examples
                - Have clear business value proposition
                - Include professional call-to-action
                - Avoid generic or vague statements

                Decision: APPROVE or REJECT
                """
            }
        ]

        decision = self.client.chat_completion(messages, self.model)

        # Extract clean content if approved
        final_approved_content = None
        if "APPROVE" in decision.upper():
            if "APPROVE:" in decision:
                final_approved_content = decision.split("APPROVE:", 1)[1].strip()
            else:
                final_approved_content = re.sub(r'^.*?APPROVE[:\s]*', '', decision, flags=re.IGNORECASE).strip()

            # Ensure tweet fits Twitter’s 280 char limit
            if len(final_approved_content) > 280:
                final_approved_content = final_approved_content[:277] + "..."

        return {
            "decision": decision,
            "attempt_number": attempt_number,
            "final_approved_content": final_approved_content,
            "agent": "boss"
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
    
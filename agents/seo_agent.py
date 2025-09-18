from utils.openrouter_client import OpenRouterClient
import os

class SEOAgent:
    def __init__(self):
        # Load authentic personal persona
        self.load_persona()
        
        self.client = OpenRouterClient()
        self.model = os.getenv('HAIKU_MODEL', 'anthropic/claude-3-haiku')
    
    def optimize_seo(self, keyword_data):
        messages = [
            {
                "role": "system",
                "content": "You are an SEO specialist for social media. Optimize content for maximum discoverability and engagement on Twitter."
            },
            {
                "role": "user",
                "content": f"""
                Content: {keyword_data['optimized_content']}
                
                Create final optimized version that:
                1. Maximizes engagement potential
                2. Uses strategic hashtag placement
                3. Optimizes for Twitter algorithm
                4. Maintains authentic voice
                5. Stays under 280 characters
                
                Return only the final tweet content, ready to post.
                """
            }
        ]
        
        seo_content = self.client.chat_completion(messages, self.model)
        
        return {
            "final_content": seo_content,
            "agent": "seo"
        }

    def optimize_seo_with_feedback(self, keyword_data, boss_feedback):
        messages = [
            {
                "role": "system",
                "content": f"""You are creating the final revision based on CEO feedback.

                PREVIOUS VERSION WAS REJECTED. Address these specific concerns:
                {boss_feedback}

                Create final version that:
                1. Includes specific metrics and concrete results
                2. Demonstrates professional expertise and credibility  
                3. Has clear business value proposition
                4. Includes strong call-to-action
                5. Maximizes engagement potential
                6. Stays under 280 characters
                7. Uses strategic hashtag placement
                8. Maintains authentic voice
                """
            },
            {
                "role": "user",
                "content": f"""
                Content: {keyword_data['optimized_content']}

                Create final optimized version addressing CEO feedback:
                - Must include specific metrics/numbers
                - Must demonstrate professional authority
                - Must have clear business value
                - Must include professional CTA
                - Must optimize for Twitter algorithm
                - Must attract potential business clients

                Return only the final tweet content, ready to post.
                This version must address all CEO concerns while maintaining engagement.
                """
            }
        ]

        seo_content = self.client.chat_completion(messages, self.model)

        return {
            "final_content": seo_content,
            "boss_feedback_addressed": boss_feedback,
            "revision": True,
            "agent": "seo"
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
    
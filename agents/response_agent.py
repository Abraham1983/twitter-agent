from utils.openrouter_client import OpenRouterClient
import os
import re

class ResponseAgent:
    def __init__(self):
        # Load authentic personal persona
        self.load_persona()
        
        self.client = OpenRouterClient()
        self.model = os.getenv('SONNET_MODEL', 'anthropic/claude-3.5-sonnet')

    def generate_response(self, comment_data, original_tweet_content=None):
        """
        Generate an authentic response to a comment using the personal persona
        
        Args:
            comment_data (dict): Contains comment text, user info, etc.
            original_tweet_content (str): The content of the original tweet being commented on
            
        Returns:
            str: The generated response content
        """
        messages = [
            {
                "role": "system",
                "content": f"""You are Abraham Vasquez (@AbrahamAv9728), an AI Platform Engineer at Autonomiq with 15+ years in tech.
                
                PERSONA DETAILS:
                - Name: {self.persona.get('name', 'Abraham Vasquez')}
                - Role: {self.persona.get('current_role', {}).get('title', 'AI Platform Engineer')} at {self.persona.get('current_role', {}).get('company', 'Autonomiq')}
                - Experience: {self.persona.get('experience', {}).get('total_years', '15+')} years in tech
                - Voice: {self.persona.get('voice', {}).get('tone', 'Professional but approachable')}
                
                KEY INSTRUCTIONS:
                1. Respond authentically as yourself, not as an AI
                2. Reference your real experience and achievements when relevant
                3. Keep responses professional but conversational
                4. Use specific metrics and concrete examples from your background
                5. Stay within your areas of expertise: AI automation, cybersecurity, cloud platforms
                6. Keep responses concise but valuable (Twitter style)
                7. Do not hallucinate - only reference real projects and experiences
                8. Maintain your authentic voice and perspective as a 42-year-old professional
                
                AVOID:
                - Generic responses like "Thanks for commenting"
                - Made-up experiences or credentials
                - Overly promotional language
                - Responses outside your areas of expertise
                
                You are responding to a comment on your tweet. Be helpful, authentic, and professional."""
            },
            {
                "role": "user",
                "content": f"""
                ORIGINAL TWEET: {original_tweet_content or 'Not available'}
                
                COMMENT TO RESPOND TO: 
                @{comment_data.get('username', 'user')}: "{comment_data.get('content', '')}"
                
                COMMENT AUTHOR ID: {comment_data.get('user_id', 'unknown')}
                
                Please provide a thoughtful, authentic response to this comment. Reference your real experience when relevant.
                Keep the response conversational and helpful. Do not exceed 280 characters.
                
                Response:"""
            }
        ]

        response = self.client.chat_completion(messages, self.model)
        
        # Clean up the response if needed
        if response and len(response) > 280:
            response = response[:277] + "..."
            
        return response

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
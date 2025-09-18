from utils.openrouter_client import OpenRouterClient
import os

class KeywordAgent:
    def __init__(self):
        # Load authentic personal persona
        self.load_persona()
        
        self.client = OpenRouterClient()
        self.model = os.getenv('HAIKU_MODEL', 'anthropic/claude-3-haiku')
    
    def optimize_keywords(self, content_data):
        messages = [
            {
                "role": "system",
                "content": "You are a keyword optimization specialist. Suggest optimal hashtags and keywords for Twitter engagement in the AI automation space."
            },
            {
                "role": "user",
                "content": f"""
                Optimize this Twitter content: {content_data['content']}
                
                Suggest 3-5 relevant hashtags focusing on:
                #AI #Automation #Python #Business #Productivity #Tech
                
                Return the content with optimized hashtags strategically placed.
                Keep the same message but enhance discoverability.
                """
            }
        ]
        
        keywords = self.client.chat_completion(messages, self.model)
        
        return {
            "optimized_content": keywords,
            "original_content": content_data['content'],
            "agent": "keyword"
        }

    def optimize_keywords_with_feedback(self, content_data, boss_feedback):
        messages = [
            {
                "role": "system",
                "content": f"""You are revising keyword optimization based on CEO feedback.

                PREVIOUS VERSION WAS REJECTED. Address these concerns:
                {boss_feedback}

                Focus on hashtags that:
                - Attract business decision makers
                - Emphasize measurable results and ROI
                - Target small business automation needs
                - Include professional service keywords
                - Highlight specific expertise and tools
                """
            },
            {
                "role": "user",
                "content": f"""
                Revise this Twitter content with better keywords: {content_data['content']}

                Based on CEO feedback, optimize for:
                - Business decision maker discovery
                - Professional service keywords
                - Results-focused hashtags
                - Industry authority positioning

                Suggested hashtags to consider:
                #BusinessAutomation #AIConsultant #ProcessOptimization #DigitalTransformation #ProductivityBoost #SmallBusiness #TechSolutions

                Return the content with strategically optimized hashtags that attract potential clients.
                Keep the same message but enhance professional discoverability.
                """
            }
        ]

        keywords = self.client.chat_completion(messages, self.model)

        return {
            "optimized_content": keywords,
            "original_content": content_data['content'],
            "boss_feedback_addressed": boss_feedback,
            "revision": True,
            "agent": "keyword"
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
    
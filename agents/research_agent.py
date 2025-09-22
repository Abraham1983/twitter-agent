from utils.openrouter_client import OpenRouterClient
import os
import random
import requests
from datetime import datetime

class ResearchAgent:
    def __init__(self):
        self.client = OpenRouterClient()
        self.model = os.getenv('HAIKU_MODEL', 'anthropic/claude-3-haiku')
        self.brave_api_key = os.getenv('BRAVE_API_KEY')
        

        # Load authentic personal persona
        self.load_persona()
        
                # Content pillars from your strategy
        self.content_pillars = [
            "education_explainer",
            "experiment_case_study", 
            "hot_take_opinion",
            "visual_framework",
            "engagement_booster",
            "personal_journey"
        ]
        
        # Monthly themes (AutonomIQ 12-month roadmap)
        self.monthly_themes = {
            1: "foundation_building",      # Jan: Set up core infrastructure
            2: "client_acquisition",       # Feb: First clients, case studies
            3: "product_refinement",       # Mar: Improve service offerings
            4: "authority_building",       # Apr: Thought leadership content
            5: "case_studies",             # May: Deep dive client results
            6: "visual_frameworks",        # Jun: Infographics, diagrams
            7: "predictive_takes",         # Jul: Industry predictions
            8: "resource_compilations",    # Aug: Tools, guides, resources
            9: "contrarian_opinions",      # Sep: Unique perspectives
            10: "thought_leadership",      # Oct: Industry influence
            11: "state_of_ai_content",     # Nov: Trends, analysis
            12: "year_recap_predictions"   # Dec: Annual review, future
        }
    
    def search_brave(self, query, count=3):
        """Search using Brave Search API for current information"""
        if not self.brave_api_key:
            return "No current search results available"
            
        headers = {
            "X-Subscription-Token": self.brave_api_key,
            "Accept": "application/json"
        }
        
        params = {
            "q": query,
            "count": count,
            "search_lang": "en",
            "country": "US"
        }
        
        try:
            response = requests.get("https://api.search.brave.com/res/v1/web/search", 
                                  headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                search_results = []
                
                for result in results.get('web', {}).get('results', []):
                    search_results.append({
                        'title': result.get('title', ''),
                        'description': result.get('description', ''),
                        'url': result.get('url', '')
                    })
                
                return search_results[:count]
            else:
                return f"Search unavailable (status: {response.status_code})"
                
        except Exception as e:
            return f"Search error: {str(e)}"

    def research_topic(self, content_type=None, day_of_month=None):
        """Enhanced research with real-time data"""
        
        # Auto-select content type if not specified
        if not content_type:
            content_type = self._select_content_type(day_of_month)
        
        # Get current month theme
        current_month = datetime.now().month
        theme = self.monthly_themes.get(current_month, "foundation_building")
        
        # Get current trends via Brave search
        search_queries = self._get_search_queries(content_type, theme)
        current_trends = {}
        
        for query_name, query in search_queries.items():
            search_results = self.search_brave(query)
            current_trends[query_name] = search_results
        
        messages = [
            {
                "role": "system",
                "content": f"""You are researching content for an AI automation business owner's Twitter.
                
                Current focus: {theme}
                Content type: {content_type}
                
                You have access to current search results to make content timely and relevant.
                Research should support building authority in AI agents, automation, and Python development.
                Target audience: Small business owners, entrepreneurs, and tech professionals."""
            },
            {
                "role": "user",
                "content": f"""
                {self._get_research_prompt(content_type, theme)}
                
                CURRENT TRENDS AND NEWS:
                {current_trends}
                
                Use this current information to make your research timely and relevant.
                Reference recent developments, case studies, or trends when appropriate.
                Focus on practical insights that help small businesses with automation.
                """
            }
        ]
        
        research = self.client.chat_completion(messages, self.model)
        
        return {
            "content_type": content_type,
            "theme": theme,
            "research": research,
            "current_trends": current_trends,
            "agent": "research"
        }
    
    def _get_search_queries(self, content_type, theme):
        """Get relevant search queries for current content"""
        
        base_queries = {
            "ai_trends": "AI automation small business trends 2024",
            "recent_news": "business automation news September 2024"
        }
        
        content_specific = {
            "education_explainer": {
                "tools": "new AI automation tools 2024 small business",
                "guides": "AI automation tutorial business 2024"
            },
            "experiment_case_study": {
                "case_studies": "AI automation success stories small business 2024",
                "results": "business automation ROI case study 2024"
            },
            "hot_take_opinion": {
                "predictions": "AI automation predictions 2025 business",
                "debates": "AI automation controversy 2024"
            },
            "visual_framework": {
                "processes": "business automation workflow examples",
                "diagrams": "AI automation process visualization"
            },
            "engagement_booster": {
                "polls": "business automation survey results 2024",
                "questions": "AI automation challenges small business"
            },
            "personal_journey": {
                "experiences": "AI automation consultant journey 2024",
                "learning": "learning AI automation business"
            }
        }
        
        queries = base_queries.copy()
        queries.update(content_specific.get(content_type, {}))
        
        return queries

    def _select_content_type(self, day_of_month):
        """Select content type based on your strategy"""
        if not day_of_month:
            day_of_month = datetime.now().day
            
        # Weekly pattern from your strategy
        day_mod = day_of_month % 7
        
        if day_mod == 0:  # Weekly thread day
            return "education_explainer"
        elif day_mod in [2, 5]:  # Visual days
            return "visual_framework"
        elif day_mod == 3:  # Hot take day
            return "hot_take_opinion"
        elif day_mod == 4:  # Engagement day
            return "engagement_booster"
        else:
            return random.choice(["experiment_case_study", "personal_journey"])
    
    def _get_research_prompt(self, content_type, theme):
        """Get specific research prompts for each content type"""
        
        prompts = {
            "education_explainer": f"""
            Research for an educational Twitter thread about AI automation.
            Theme: {theme}
            
            Provide:
            - 3 key concepts to explain simply
            - Real-world examples for small businesses
            - Common misconceptions to address
            - Actionable takeaways for entrepreneurs
            
            Focus on practical automation that saves time and money.
            """,
            
            "experiment_case_study": f"""
            Research for sharing an AI automation experiment/case study.
            Theme: {theme}
            
            Provide:
            - Realistic automation scenario for small business
            - Expected challenges and solutions
            - Measurable outcomes (time saved, cost reduced)
            - Lessons learned format
            - Tools or technologies used
            """,
            
            "hot_take_opinion": f"""
            Research for a contrarian/bold opinion about AI automation.
            Theme: {theme}
            
            Provide:
            - Common belief about AI/automation to challenge
            - Supporting evidence for contrarian view
            - Future prediction for business automation
            - Discussion-worthy angle that attracts engagement
            """,
            
            "visual_framework": f"""
            Research for a visual framework/diagram about AI automation.
            Theme: {theme}
            
            Provide:
            - Process or concept that needs visualization
            - 3-5 key components/steps
            - Simple analogies for business owners
            - Visual description for diagram
            - How this helps businesses
            """,
            
            "engagement_booster": f"""
            Research for an engagement-focused post (poll, question, etc).
            Theme: {theme}
            
            Provide:
            - Interesting question about AI automation for businesses
            - Poll options that spark debate
            - Community discussion starter
            - Relatable scenarios for entrepreneurs
            """,
            
            "personal_journey": f"""
            Research for personal journey/behind-the-scenes content.
            Theme: {theme}
            
            Provide:
            - Realistic learning experience with automation
            - Wins and failures to share authentically
            - Relatable struggles for business owners
            - Growth mindset message
            - What you're building/testing next
            """
        }
        
        return prompts.get(content_type, prompts["education_explainer"])

    def research_topic_with_feedback(self, content_type, boss_feedback, day_of_month=None):
        """Enhanced research incorporating boss feedback for revision"""

        # Auto-select content type if not specified
        if not content_type:
            content_type = self._select_content_type(day_of_month)

        # Get current month theme
        current_month = datetime.now().month
        theme = self.monthly_themes.get(current_month, "foundation_building")

        # Get current trends via Brave search
        search_queries = self._get_search_queries(content_type, theme)
        current_trends = {}

        for query_name, query in search_queries.items():
            search_results = self.search_brave(query)
            current_trends[query_name] = search_results

        messages = [
            {
                "role": "system",
                "content": f"""You are researching content for an AI automation business owner's Twitter.

                Current focus: {theme}
                Content type: {content_type}

                IMPORTANT: You are revising based on CEO feedback. The previous version was rejected.

                CEO FEEDBACK TO ADDRESS:
                {boss_feedback}

                Focus on finding:
                - Specific metrics and concrete results
                - Professional credibility markers  
                - Unique insights and expertise demonstrations
                - Clear business value propositions
                - Real client case studies and examples

                Research should support building authority in AI agents, automation, and Python development.
                Target audience: Small business owners, entrepreneurs, and tech professionals."""
            },
            {
                "role": "user",
                "content": f"""
                {self._get_research_prompt(content_type, theme)}

                CURRENT TRENDS AND NEWS:
                {current_trends}

                REVISION REQUIREMENTS BASED ON CEO FEEDBACK:
                1. Find specific metrics (time saved, cost reduced, efficiency gained)
                2. Research concrete automation examples with measurable outcomes
                3. Look for professional credibility elements (certifications, tools mastery)
                4. Find unique business insights that differentiate from competitors
                5. Identify clear value propositions for small business owners

                Use this current information to make research timely, relevant, and address all CEO concerns.
                Focus on practical insights with specific numbers and proven results.
                """
            }
        ]

        research = self.client.chat_completion(messages, self.model)

        return {
            "content_type": content_type,
            "theme": theme,
            "research": research,
            "current_trends": current_trends,
            "boss_feedback_addressed": boss_feedback,
            "revision": True,
            "agent": "research"
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
            print("✅ Loaded authentic persona for Abraham Vasquez")
        except ImportError:
            print("⚠️  Could not load persona file")
            self.persona = {}
            self.authentic_phrases = []
    
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def chat_completion(self, messages, model="anthropic/claude-3-haiku"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.7
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            print(f"API Error: {result}")
            return "Error: Could not get response from AI"

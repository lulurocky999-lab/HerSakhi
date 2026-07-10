import os
import requests
import logging
from django.conf import settings
from .exceptions import AIProviderException

logger = logging.getLogger(__name__)

from dotenv import load_dotenv

class OpenRouterProvider:
    def __init__(self):
        # Force reload environment variables to catch .env updates without server restart
        load_dotenv(settings.BASE_DIR / '.env', override=True)
        
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = os.getenv('OPENROUTER_MODEL', "openrouter/free")
        self.http_referer = os.getenv('OPENROUTER_HTTP_REFERER', "http://localhost:8000")
        self.title = os.getenv('OPENROUTER_TITLE', "NagarNetra")
        self.reasoning_enabled = os.getenv('OPENROUTER_REASONING_ENABLED', "true").lower() == "true"
        
    def generate(self, messages, use_fallback=False, temperature=0.7):
        if not self.api_key:
            raise AIProviderException("OPENROUTER_API_KEY is not configured")
            
        # We ignore use_fallback now since we want to strictly use the ENV model
        model = self.model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.http_referer,
            "X-Title": self.title,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API error: {e}")
            if not use_fallback:
                logger.info("Attempting fallback model...")
                return self.generate(messages, use_fallback=True, temperature=temperature)
            raise AIProviderException(f"AI provider failed after fallback: {e}")

# Factory function to get the configured provider
def get_ai_provider():
    return OpenRouterProvider()

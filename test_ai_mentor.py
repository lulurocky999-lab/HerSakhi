import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ai.services import chat_with_mentor
from ai.providers import get_ai_provider

def test():
    # Let's see what the raw provider gives first
    provider = get_ai_provider()
    system_prompt = (
        "You are HerSakhi, an empathetic, highly intelligent AI Career Mentor. "
        "Use the provided User Context to give highly personalized, specific advice. "
        "Do not be generic. Reference their specific goals, skills, and roadmap. "
        "Return ONLY a JSON object with: 'reply' (string) and 'suggested_actions' (list of strings, optional)."
    )
    user_prompt = "User Context:\n{}\n\nChat History:\n\n\nUser: hi"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    raw = provider.generate(messages)
    print("RAW OUTPUT:", raw)
    
    print("\n\nTesting service function:")
    res = chat_with_mentor([], "hi", {})
    print("SERVICE RESULT:", res)

if __name__ == '__main__':
    test()

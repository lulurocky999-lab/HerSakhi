import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ai.providers import get_ai_provider

def test_ai():
    provider = get_ai_provider()
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Please output a valid JSON object with a single key 'status' and value 'success'."},
        {"role": "user", "content": "Test the connection."}
    ]
    try:
        response = provider.generate(messages)
        print(f"Success! Model output: {response}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == '__main__':
    test_ai()

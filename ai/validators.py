import json
from .exceptions import AIValidationException
import re

def validate_json_response(response_text: str) -> dict:
    """Extracts and validates JSON from AI response, ignoring markdown or pleasantries."""
    try:
        text = response_text.strip()
        
        # Try finding JSON object {}
        start_obj = text.find('{')
        end_obj = text.rfind('}')
        
        # Try finding JSON array []
        start_arr = text.find('[')
        end_arr = text.rfind(']')
        
        if start_obj != -1 and end_obj != -1 and end_obj >= start_obj:
            # If there's an array that encapsulates the object, use the array
            if start_arr != -1 and start_arr < start_obj and end_arr > end_obj:
                text = text[start_arr:end_arr+1]
            else:
                text = text[start_obj:end_obj+1]
        elif start_arr != -1 and end_arr != -1 and end_arr >= start_arr:
            text = text[start_arr:end_arr+1]
            
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise AIValidationException(f"Failed to parse AI response as JSON: {e}\nRaw output: {response_text}")
    except Exception as e:
        raise AIValidationException(f"Unexpected error validating JSON: {e}")

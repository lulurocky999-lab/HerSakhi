from .providers import get_ai_provider
from .validators import validate_json_response
import logging
import json

logger = logging.getLogger(__name__)

def generate_ai_response(system_prompt: str, user_prompt: str) -> dict:
    """
    Core function to communicate with AI provider and return parsed JSON.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    provider = get_ai_provider()
    try:
        response_text = provider.generate(messages)
        return validate_json_response(response_text)
    except Exception as e:
        logger.error(f"AI Service Failure: {e}")
        try:
            with open(r'c:\Users\HP\Desktop\HerSakhi\ai_debug.txt', 'a', encoding='utf-8') as f:
                f.write(f"ERROR: {str(e)}\n")
        except:
            pass
        # Always return structured failure instead of crashing
        return {
            "success": False,
            "message": "AI service is currently unavailable.",
            "error": str(e)
        }

def analyze_resume(resume_text: str, target_role: str) -> dict:
    system_prompt = (
        "You are an expert ATS (Applicant Tracking System) and Career Coach. "
        "Analyze the provided resume against the target role and extract structured information. "
        "Return ONLY a JSON object with EXACTLY the following structure:\n"
        "{\n"
        "  \"ats_score\": <int 0-100>,\n"
        "  \"score_breakdown\": {\n"
        "    \"format\": <int 0-100>, \"content\": <int 0-100>, \"skills\": <int 0-100>, \"experience\": <int 0-100>, \"keywords\": <int 0-100>\n"
        "  },\n"
        "  \"strengths\": [<list of 2-4 strings>],\n"
        "  \"improvements\": [<list of 2-4 strings>],\n"
        "  \"keyword_match\": <int 0-100>,\n"
        "  \"target_role\": <string, inferred or provided target role>,\n"
        "  \"suggestions\": [<list of 2-4 string actionable suggestions>],\n"
        "  \"parsed_resume\": {\n"
        "    \"name\": <string>,\n"
        "    \"role\": <string>,\n"
        "    \"email\": <string>,\n"
        "    \"phone\": <string>,\n"
        "    \"location\": <string>,\n"
        "    \"linkedin\": <string or null>,\n"
        "    \"github\": <string or null>,\n"
        "    \"summary\": <string>,\n"
        "    \"skills\": [<list of strings>],\n"
        "    \"experience\": [{\"role\": <string>, \"company\": <string>, \"duration\": <string>, \"location\": <string>, \"bullets\": [<list of strings>]}],\n"
        "    \"education\": [{\"degree\": <string>, \"institution\": <string>, \"duration\": <string>, \"gpa\": <string or null>}]\n"
        "  }\n"
        "}"
    )
    user_prompt = f"Target Role: {target_role}\n\nResume Text:\n{resume_text}"
    return generate_ai_response(system_prompt, user_prompt)

def generate_career_roadmap(user_context: dict) -> dict:
    system_prompt = (
        "You are a Senior Career Strategist. Based on the user's profile, assessment, and resume data, "
        "generate a personalized 4-phase career roadmap. "
        "Return ONLY a JSON object with: 'estimated_finish' (string, e.g. '6 months'), "
        "'phases' (list of objects, each with 'title', 'description', 'order' (int starting at 1))."
    )
    user_prompt = f"User Context:\n{json.dumps(user_context, indent=2)}"
    return generate_ai_response(system_prompt, user_prompt)

def analyze_skill_gap(current_skills: list, target_role: str) -> dict:
    system_prompt = (
        "You are a Technical Recruiter and Educator. Compare the user's current skills to the requirements of the target role. "
        "Return ONLY a JSON object with EXACTLY this structure:\n"
        "{\n"
        "  \"match_pct\": <int 0-100>,\n"
        "  \"match_label\": <string, e.g. 'Good Match'>,\n"
        "  \"match_change\": <string, e.g. '+5%'>,\n"
        "  \"skills_have\": <int>,\n"
        "  \"skills_improve\": <int>,\n"
        "  \"skills_lack\": <int>,\n"
        "  \"target_role\": {\n"
        "    \"title\": <string>,\n"
        "    \"industry\": <string>,\n"
        "    \"experience\": <string>,\n"
        "    \"match_pct\": <int 0-100>,\n"
        "    \"total_required\": <int>,\n"
        "    \"have\": <int>,\n"
        "    \"improve\": <int>,\n"
        "    \"lack\": <int>\n"
        "  },\n"
        "  \"breakdown\": [\n"
        "    {\"category\": <string>, \"have\": <int 0-100>, \"improve\": <int 0-100>, \"lack\": <int 0-100>}\n"
        "  ],\n"
        "  \"top_gaps\": [\n"
        "    {\"skill\": <string>, \"level\": <string 'High'|'Medium'|'Low'>, \"current\": <int 0-100>, \"required\": <int 0-100>, \"impact\": <int 1-5>}\n"
        "  ],\n"
        "  \"next_steps\": [\n"
        "    {\"theme\": <string 'success'|'primary'|'warning'>, \"title\": <string>, \"desc\": <string>, \"badge\": <string>}\n"
        "  ]\n"
        "}"
    )
    user_prompt = f"Target Role: {target_role}\nCurrent Skills: {json.dumps(current_skills)}"
    return generate_ai_response(system_prompt, user_prompt)

def extract_career_insights(assessment_json: dict) -> dict:
    system_prompt = (
        "You are a Career Psychologist. Analyze the user's career assessment responses. "
        "Return ONLY a JSON object with: 'career_readiness_score' (int 0-100), 'top_strengths' (list of strings), "
        "'primary_work_style' (string), and 'actionable_insight' (string)."
    )
    user_prompt = f"Assessment Data:\n{json.dumps(assessment_json, indent=2)}"
    return generate_ai_response(system_prompt, user_prompt)

def chat_with_mentor(history: list, user_message: str, user_context: dict) -> dict:
    system_prompt = (
        "You are HerSakhi, an empathetic, highly intelligent AI Career Mentor. "
        "Use the provided User Context to give highly personalized, specific advice. "
        "Do not be generic. Reference their specific goals, skills, and roadmap. "
        "Return ONLY a JSON object with: 'reply' (string) and 'suggested_actions' (list of strings, optional)."
    )
    context_str = json.dumps(user_context, indent=2)
    history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
    
    user_prompt = f"User Context:\n{context_str}\n\nChat History:\n{history_str}\n\nUser: {user_message}"
    return generate_ai_response(system_prompt, user_prompt)

def extract_opportunities(user_profile: dict) -> dict:
    system_prompt = (
        "You are an Opportunity Matchmaker. Based on the user's profile and goals, "
        "generate 5 highly relevant opportunities (jobs, internships, hackathons). "
        "Return ONLY a JSON object with an 'opportunities' list. "
        "Each opportunity must have: 'title', 'company', 'location', 'type' (e.g. Internship), 'time_left' (e.g. '2d left')."
    )
    user_prompt = f"User Profile:\n{json.dumps(user_profile, indent=2)}"
    return generate_ai_response(system_prompt, user_prompt)

# Pydantic models for structured output validation (to be used later if needed)
from pydantic import BaseModel
from typing import List, Optional

class SkillGapResult(BaseModel):
    current_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]

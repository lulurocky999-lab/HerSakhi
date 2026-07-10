class AIServiceException(Exception):
    """Base exception for AI Service errors"""
    pass

class AIProviderException(AIServiceException):
    """Raised when an AI provider fails"""
    pass

class AIValidationException(AIServiceException):
    """Raised when AI output fails validation"""
    pass

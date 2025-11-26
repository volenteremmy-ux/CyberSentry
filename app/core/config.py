from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ulinzi Trust SDK"
    VERSION: str = "2.3.0 (Stable-Fix)"
    API_PREFIX: str = "/api/v1"
    
    # Thresholds
    CRITICAL_SCORE: int = 80
    WARNING_SCORE: int = 40

    # --- AI CASCADING SETTINGS ---
    # 1. Hugging Face (Switched to Facebook BART - Works on new Router)
    HF_API_KEY: str 
    HF_MODEL_URL: str = "https://router.huggingface.co/models/facebook/bart-large-mnli"
    HF_TIMEOUT: int = 4  # Increased slightly for reliability

    # 2. Google Gemini (Switched to 'gemini-pro' - Most stable version)
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash" 
    GEMINI_TIMEOUT: int = 4 

    class Config:
        case_sensitive = True
        env_file = ".env" 

settings = Settings()
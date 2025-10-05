import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for Claude SDK"""
    
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-20250514")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration exists"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment. "
                "Please create .env file from .env.example"
            )
        return True

from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Environment
    ENV: str = os.getenv("ENV", "development")
    
    # Current PostgreSQL Database (for local development)
    POSTGRES_DATABASE_URL: str = os.getenv(
        "POSTGRES_DATABASE_URL",
        "postgresql://user:password@localhost:5432/ai_agent"
    )
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_DATABASE_URL: str = os.getenv("SUPABASE_DATABASE_URL", "")

    @property
    def DATABASE_URL(self) -> str:
        """Get the appropriate database URL based on environment."""
        if self.ENV == "production":
            if not self.SUPABASE_DATABASE_URL:
                raise ValueError("SUPABASE_DATABASE_URL must be set in production")
            return self.SUPABASE_DATABASE_URL
        return self.POSTGRES_DATABASE_URL

@lru_cache()
def get_settings():
    return Settings() 
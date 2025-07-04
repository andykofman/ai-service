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

    # Generic database URL that can override others (useful for platforms like
    # Vercel)
    DATABASE_URL_ENV: str | None = os.getenv("DATABASE_URL")
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_DATABASE_URL: str = os.getenv("SUPABASE_DATABASE_URL", "")

    @property
    def DATABASE_URL(self) -> str:
        """Get the appropriate database URL based on environment."""
        # If a DATABASE_URL environment variable is provided, prefer it
                    
        # If DATABASE_URL_ENV exists, use it
        # If in production and SUPABASE_DATABASE_URL exists, use it
        # Otherwise, use the local POSTGRES_DATABASE_URL

        if self.DATABASE_URL_ENV:
            return self.DATABASE_URL_ENV

        if self.ENV == "production":
            if not self.SUPABASE_DATABASE_URL:
                raise ValueError("SUPABASE_DATABASE_URL must be set in production")
            return self.SUPABASE_DATABASE_URL

        return self.POSTGRES_DATABASE_URL

@lru_cache()
def get_settings():
    return Settings() 


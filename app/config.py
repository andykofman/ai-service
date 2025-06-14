from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Current PostgreSQL Database
    POSTGRES_DATABASE_URL: str = os.getenv(
        "POSTGRES_DATABASE_URL",
        "postgresql://user:password@localhost:5432/ai_agent"
    )
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_DATABASE_URL: str = os.getenv("SUPABASE_DATABASE_URL", "")

@lru_cache()
def get_settings():
    return Settings() 
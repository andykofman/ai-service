from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
from supabase import create_client, Client
from functools import lru_cache

settings = get_settings()

# Database Engine (will use either PostgreSQL or Supabase based on environment)
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

@lru_cache()
def get_supabase() -> Client:
    """Get or create Supabase client instance."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Supabase URL and Key must be set in environment variables")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
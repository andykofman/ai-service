import pytest
from app.db.database import get_supabase
from app.config import get_settings

def test_supabase_connection():
    settings = get_settings()
    
    # Skip test if Supabase credentials are not configured
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        pytest.skip("Supabase credentials not configured")
    
    try:
        # Test the connection
        supabase = get_supabase()
        response = supabase.table('users').select("*").limit(1).execute()
        print("Connection successful!")
        assert response is not None
    except Exception as e:
        pytest.fail(f"Connection failed: {str(e)}")
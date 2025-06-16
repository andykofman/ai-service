from sqlalchemy.orm import Session
from app.models import models
import logging

logger = logging.getLogger(__name__)

def ensure_user_exists(db: Session, user_id: str):
    try:
        user = db.query(models.User).filter_by(user_id=user_id).first()
        if not user:
            logger.debug(f"Creating new user with ID: {user_id}")
            user = models.User(user_id=user_id, name="Test User", email="test@example.com")
            db.add(user)
            db.commit()
            logger.debug("New user created successfully")
    except Exception as e:
        logger.error(f"Database error while handling user: {str(e)}")

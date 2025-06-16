import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import models
import logging

logger = logging.getLogger(__name__)

def save_conversation(db: Session, user_id: str, user_msg: str, bot_reply: str):
    now = datetime.now(timezone.utc).isoformat()
    try:
        # Save user message
        user_entry = models.Conversation(
            conv_id=str(uuid.uuid4()),
            user_id=user_id,
            timestamp=now,
            message=user_msg,
            direction="in"
        )
        db.add(user_entry)

        # Save bot response
        bot_entry = models.Conversation(
            conv_id=str(uuid.uuid4()),
            user_id=user_id,
            timestamp=now,
            message=bot_reply,
            direction="out"
        )
        db.add(bot_entry)

        db.commit()
        logger.debug("Conversation saved successfully")
    except Exception as e:
        logger.error(f"Error saving conversation: {str(e)}")

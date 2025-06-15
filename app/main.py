from fastapi import FastAPI, Depends, staticfiles
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from app.routes import users, orders, products
from app.db.database import Base, engine, get_db
from app.models import models
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from pydantic import ConfigDict
import os
import logging
from app.ai.intent_router import detect_intent_with_ai
from dotenv import load_dotenv
from app.config import get_settings
from fastapi import HTTPException

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables and settings
settings = get_settings()
logger.debug("Settings loaded")

# Create DB tables only in development
if settings.ENV == "development":
    Base.metadata.create_all(bind=engine)
    logger.debug("Database tables created in development mode")

app = FastAPI()

#include the routers
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)

#static files
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")

# Request schema
class MessageRequest(BaseModel):
    user_id: str
    message: str

# Dummy logic handlers
def get_order_status(user_id):
    return f"Order for {user_id}: Shipped, expected delivery June 15"

def update_profile(user_id):
    return f"Profile for {user_id} has been updated (dummy response)."

def search_products(user_id):
    return f"Here are some product suggestions for {user_id}."

# Intent routing
def detect_intent(message: str):
    message = message.lower()
    if "order" in message or "status" in message:
        return "get_order_status"
    elif "update" in message or "email" in message:
        return "update_profile"
    elif "laptop" in message or "search" in message or "product" in message:
        return "search_products"
    else:
        return "unknown"

#webhook is the endpoint that receives the messages from the user
#req is the request body
#user_id is the id of the user
#message is the message from the user
#intent is the intent of the user
#reply is the response to the user

@app.post("/webhook")
async def webhook(req: MessageRequest, db: Session = Depends(get_db)):
    try:
        user_id = req.user_id
        message = req.message
        
        logger.debug(f"Environment: {settings.ENV}")
        logger.debug(f"Database URL configured: {'Yes' if settings.DATABASE_URL else 'No'}")
        logger.debug(f"Supabase configured: {'Yes' if settings.SUPABASE_URL and settings.SUPABASE_KEY else 'No'}")
        logger.debug(f"HF API Token configured: {'Yes' if HF_API_TOKEN else 'No'}")
        logger.debug(f"Processing webhook request for user {user_id} with message: {message}")
        
        #save the user to the database
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
            raise HTTPException(status_code=500, detail="Database error while handling user")

        #detect the intent of the user
        try:
            intent = detect_intent_with_ai(message)
            logger.debug(f"Detected intent: {intent}")
        except Exception as e:
            logger.error(f"Error detecting intent: {str(e)}")
            logger.error(f"Full error details: {repr(e)}")
            intent = "unknown"

        if intent == "search_products":
            try:
                products = db.query(models.Product).all()
                reply = [f"{p.name} - ${p.price}" for p in products]
            except Exception as e:
                logger.error(f"Error fetching products: {str(e)}")
                reply = "Sorry, I couldn't fetch the products at the moment."
        elif intent == "place_order":
            reply = "Please use the 'Place Order' feature in the interface."
        elif intent == "update_profile":
            reply = "Please use the 'Update Profile' option to modify your info."
        elif intent == "get_order_status":
            reply = "Please provide your order ID in the 'Order Status' section."
        else:
            reply = "Sorry, I didn't understand your request."

        now = datetime.now(timezone.utc).isoformat()
        
        try:
            # Save user message
            user_msg = models.Conversation(
                conv_id=str(uuid.uuid4()),
                user_id=user_id,
                timestamp=now,
                message=message,
                direction="in"
            )
            db.add(user_msg)

            # Save bot response
            bot_msg = models.Conversation(
                conv_id=str(uuid.uuid4()),
                user_id=user_id,
                timestamp=now,
                message=reply,
                direction="out"
            )
            db.add(bot_msg)

            db.commit()
            logger.debug("Conversation saved successfully")
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            # Don't raise here, we still want to return the response even if saving fails

        return JSONResponse(content={"response": reply})
    except Exception as e:
        logger.error(f"Unexpected error in webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

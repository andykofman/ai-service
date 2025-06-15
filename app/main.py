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
        logger.debug(f"Processing webhook request for user {user_id} with message: {message}")
        
        # save the user to the database (best effort)
        try:
            user = db.query(models.User).filter_by(user_id=user_id).first()
            if not user:
                logger.debug(f"Creating new user with ID: {user_id}")
                user = models.User(user_id=user_id, name="Test User", email="test@example.com")
                db.add(user)
                db.commit()
                logger.debug("New user created successfully")
        except Exception as e:
            # Log the error but continue so the request still succeeds
            logger.error(f"Database error while handling user: {str(e)}")

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
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")
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
import random
from typing import Optional

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

# Add a simple in-memory state management for conversation context
class ConversationState:
    def __init__(self):
        self.user_states = {}  # user_id -> state dict

    def get_state(self, user_id: str) -> dict:
        if user_id not in self.user_states:
            self.user_states[user_id] = {
                "awaiting_product_selection": False,
                "awaiting_browse_confirmation": False,
                "last_products_shown": [],
                "last_intent": None
            }
        return self.user_states[user_id]

    def clear_state(self, user_id: str):
        if user_id in self.user_states:
            self.user_states[user_id] = {
                "awaiting_product_selection": False,
                "awaiting_browse_confirmation": False,
                "last_products_shown": [],
                "last_intent": None
            }

conversation_state = ConversationState()

def get_user_orders(db: Session, user_id: str):
    return db.query(models.Order).filter_by(user_id=user_id).all()

def get_all_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_name(db: Session, product_name: str) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.name.ilike(f"%{product_name}%")).first()

def create_order(db: Session, user_id: str, product_id: str):
    order = models.Order(
        order_id=str(uuid.uuid4()),
        user_id=user_id,
        product_id=product_id,
        quantity=1,
        status="pending"
    )
    db.add(order)
    db.commit()
    return order

# Intent routing
#redundant code, but keeping for reference
""" 
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

"""

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
        state = conversation_state.get_state(user_id)
        
        logger.debug(f"Environment: {settings.ENV}")
        logger.debug(f"Database URL configured: {'Yes' if settings.DATABASE_URL else 'No'}")
        logger.debug(f"Supabase configured: {'Yes' if settings.SUPABASE_URL and settings.SUPABASE_KEY else 'No'}")
        logger.debug(f"Processing webhook request for user {user_id} with message: {message}")
        
        # Handle browse confirmation first
        if state["awaiting_browse_confirmation"]:
            if message.lower() in ["yes", "show products", "show me products"]:
                products = get_all_products(db)
                if not products:
                    reply = "I'm sorry, but there are no products available at the moment."
                    conversation_state.clear_state(user_id)
                else:
                    state["last_products_shown"] = products
                    state["awaiting_product_selection"] = True
                    state["awaiting_browse_confirmation"] = False
                    reply = "Here are our available products:\n" + "\n".join([f"- {p.name} (${p.price})" for p in products]) + "\n\nPlease type the name of the product you'd like to order."
            else:
                reply = "I'm not sure I understand. Would you like to see our available products? (Just say 'yes' or 'show products')"
            return JSONResponse(content={"response": reply})

        # Handle product selection if we're in that state
        if state["awaiting_product_selection"]:
            product = get_product_by_name(db, message)
            if product:
                # Create the order
                order = create_order(db, user_id, product.product_id)
                conversation_state.clear_state(user_id)
                reply = f"Great! I've placed an order for {product.name}. Your order ID is {order.order_id}. Would you like to check your order status?"
            else:
                # Check if this is a browse request
                if message.lower() in ["yes", "show products", "show me products"]:
                    products = get_all_products(db)
                    if not products:
                        reply = "I'm sorry, but there are no products available at the moment."
                        conversation_state.clear_state(user_id)
                    else:
                        state["last_products_shown"] = products
                        reply = "Here are our available products:\n" + "\n".join([f"- {p.name} (${p.price})" for p in products]) + "\n\nPlease type the name of the product you'd like to order."
                else:
                    reply = "I couldn't find that product. Here are the available products again:\n" + "\n".join([f"- {p.name} (${p.price})" for p in state["last_products_shown"]])
            return JSONResponse(content={"response": reply})

        # Save the user to the database (best effort)
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

        # Detect the intent
        try:
            intent = detect_intent_with_ai(message)
            logger.debug(f"Detected intent: {intent}")
            state["last_intent"] = intent
        except Exception as e:
            logger.error(f"Error detecting intent: {str(e)}")
            intent = "unknown"

        # Handle different intents
        if intent == "search_products":
            products = get_all_products(db)
            if not products:
                reply = "I'm sorry, but there are no products available at the moment."
                conversation_state.clear_state(user_id)
            else:
                state["last_products_shown"] = products
                state["awaiting_product_selection"] = True
                reply = "Here are our available products:\n" + "\n".join([f"- {p.name} (${p.price})" for p in products]) + "\n\nPlease type the name of the product you'd like to order."
        
        elif intent == "get_order_status":
            orders = get_user_orders(db, user_id)
            if not orders:
                reply = "You don't have any orders yet. Would you like to see our available products? (Just say 'yes' or 'show products')"
                state["awaiting_browse_confirmation"] = True
            else:
                order_details = []
                for order in orders:
                    product = db.query(models.Product).filter_by(product_id=order.product_id).first()
                    if product:
                        order_details.append(f"Order {order.order_id}: {product.name} - Status: {order.status}")
                reply = "Here are your orders:\n" + "\n".join(order_details)
                conversation_state.clear_state(user_id)
        
        elif intent == "place_order":
            products = get_all_products(db)
            if not products:
                reply = "I'm sorry, but there are no products available at the moment."
                conversation_state.clear_state(user_id)
            else:
                state["last_products_shown"] = products
                state["awaiting_product_selection"] = True
                reply = "Here are our available products:\n" + "\n".join([f"- {p.name} (${p.price})" for p in products]) + "\n\nPlease type the name of the product you'd like to order."
        
        elif intent == "greeting":
            greetings = [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Welcome! How may I assist you?",
                "Greetings! How can I be of service?"
            ]
            reply = random.choice(greetings)
            conversation_state.clear_state(user_id)
        
        elif intent == "farewell":
            farewells = [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye for now! Come back soon!",
                "Farewell! It was nice chatting with you!"
            ]
            reply = random.choice(farewells)
            conversation_state.clear_state(user_id)
        
        else:
            reply = "I'm not sure I understand. You can ask me about your orders, browse products, or place a new order."
            conversation_state.clear_state(user_id)

        # Save the conversation
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

        return JSONResponse(content={"response": reply})
    except Exception as e:
        logger.error(f"Unexpected error in webhook: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from app.routes import users, orders, products
from app.db.database import Base, engine, get_db
from app.models import models
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session

#  create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

#include the routers
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)
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
    user_id = req.user_id
    message = req.message
    
    #save the user to the database
    #if the user is not in the database, create a new user
    #if the user is in the database, update the user
    user = db.query(models.User).filter_by(user_id=user_id).first()
    if not user:
        user = models.User(user_id=user_id, name="Test User", email="test@example.com")
        db.add(user)
        db.commit()

    db.commit()

    #detect the intent of the user
    intent = detect_intent(message)

    if intent == "get_order_status":
        reply = get_order_status(user_id)
    elif intent == "update_profile":
        reply = update_profile(user_id)
    elif intent == "search_products":
        reply = search_products(user_id)
    else:
        reply = "Sorry, I didn't understand your request."

    now = datetime.now(timezone.utc).isoformat()
    #save the conversation to the database
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

    return JSONResponse(content={"response": reply})

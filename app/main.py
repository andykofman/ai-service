from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.db.database import Base, engine
from app.models import models


#  create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.post("/webhook")
async def webhook(req: MessageRequest):
    user_id = req.user_id
    message = req.message

    intent = detect_intent(message)

    if intent == "get_order_status":
        reply = get_order_status(user_id)
    elif intent == "update_profile":
        reply = update_profile(user_id)
    elif intent == "search_products":
        reply = search_products(user_id)
    else:
        reply = "Sorry, I didn’t understand your request."

    return JSONResponse(content={"response": reply})

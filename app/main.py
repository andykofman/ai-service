from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class MessageRequest(BaseModel):
    user_id: str
    message: str



#Dummy function to get the order status
def get_order_sttus(user_id: str):
    return f"Order status for {user_id} is: Shipped, expected delivery date: 2025-06-15"


def update_profile(user_id:str):
    return f"Profile for {user_id} has been updated"


def search_products(user_id:str):
    return f"Here are some products that you might like: Product 1, Product 2, Product 3 for {user_id}"


#Intent detection (Naive)
def intent_detection(message:str):
    if "order" in message.lower() or "status" in message.lower():
        return "order"
    elif "profile" in message.lower() or "update" in message.lower() or "email" in message.lower() or "phone" in message.lower() or "address" in message.lower():
        return "profile"
    elif "search" in message.lower() or "product" in message.lower() or "buy" in message.lower():
        return "search"
    else:
        return "unknown"



@app.post("/webhook") #this is the endpoint for the webhook
 #this is the function that will be called when the webhook is triggered
async def webhook(request: MessageRequest): 

    # Dummy request
    user_id = request.user_id #this is the user id
    message = request.message #this is the message from the user

    intent = intent_detection(message)

    if intent == "order":
        response = get_order_sttus(user_id)
    elif intent == "profile":
        response = update_profile(user_id)
    elif intent == "search":
        response = search_products(user_id)
    else:
        response = "I'm sorry, I don't understand your request" 

    return JSONResponse(content={"response": response})

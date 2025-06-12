from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class MessageRequest(BaseModel):
    user_id: str
    message: str

@app.post("/webhook") #this is the endpoint for the webhook
async def webhook(request: MessageRequest): #this is the function that will be called when the webhook is triggered

    # Dummy request
    user_id = request.user_id #this is the user id
    message = request.message #this is the message from the user

    # Dummy response
    reply = f"Hello {user_id}, you said: '{message}'"

    return JSONResponse(content={"response": reply}) #this is the response to the user

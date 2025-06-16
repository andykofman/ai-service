from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import random
import logging

from app.db.database import get_db
from app.schemas.request import MessageRequest
from app.services.conversation_state import ConversationState
from app.services.conversation import save_conversation
from app.services.intent_handlers import (
    get_user_orders,
    get_all_products,
    get_product_by_name,
    create_order
)
from app.ai.intent_router import detect_intent_with_ai
from app.services.user_service import ensure_user_exists
from app.models import models

router = APIRouter()
logger = logging.getLogger(__name__)
conversation_state = ConversationState()

@router.post("/webhook")
async def webhook(req: MessageRequest, db: Session = Depends(get_db)):
    user_id = req.user_id
    message = req.message
    state = conversation_state.get_state(user_id)

    ensure_user_exists(db, user_id)

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
        save_conversation(db, user_id, message, reply)
        return JSONResponse(content={"response": reply})

    if state["awaiting_product_selection"]:
        product = get_product_by_name(db, message)
        if product:
            order = create_order(db, user_id, product.product_id)
            conversation_state.clear_state(user_id)
            reply = f"Great! I've placed an order for {product.name}. Your order ID is {order.order_id}. Would you like to check your order status?"
        else:
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
        save_conversation(db, user_id, message, reply)
        return JSONResponse(content={"response": reply})

    try:
        intent = detect_intent_with_ai(message)
        state["last_intent"] = intent
    except Exception as e:
        logger.error(f"Error detecting intent: {str(e)}")
        intent = "unknown"

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
        reply = random.choice([
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Welcome! How may I assist you?",
            "Greetings! How can I be of service?"
        ])
        conversation_state.clear_state(user_id)

    elif intent == "farewell":
        reply = random.choice([
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Bye for now! Come back soon!",
            "Farewell! It was nice chatting with you!"
        ])
        conversation_state.clear_state(user_id)

    else:
        reply = "I'm not sure I understand. You can ask me about your orders, browse products, or place a new order."
        conversation_state.clear_state(user_id)

    save_conversation(db, user_id, message, reply)
    return JSONResponse(content={"response": reply})

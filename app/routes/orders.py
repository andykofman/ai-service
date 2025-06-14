from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Order
from app.db.database import get_db
from pydantic import BaseModel, Field
from typing import List, Literal
import uuid
from pydantic import ConfigDict
from app.models.models import Order, User, Product

#API Router is used to define the routes for the orders
#router is used to define the routes for the orders
router = APIRouter()

# Pydantic models for request/response
class OrderBase(BaseModel):
    product_id: str
    user_id: str
    quantity: int = Field(..., gt=0) #greater than 0
    status: Literal["pending", "shipped", "delivered", "cancelled"] 

    model_config = ConfigDict(from_attributes=True) #This enables Pydantic to convert the SQLAlchemy model to a Pydantic model (ORM mode)

# Create API layer for the order
#input
class OrderCreate(OrderBase):
    pass
#output
class OrderResponse(OrderBase):
    order_id: str


#Routes

@router.get("/orders", response_model=List[OrderResponse])
#get_orders is the endpoint that returns all the orders
def get_orders(db: Session = Depends(get_db)): 
    return db.query(Order).all()

@router.get("/orders/{order_id}", response_model=OrderResponse)
#get_order is the endpoint that returns a specific order
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter_by(order_id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders", response_model=OrderResponse)
#create_order is the endpoint that creates a new order
def create_order(order:OrderCreate, db: Session = Depends(get_db)):
    #Step 1: validate user exists
    user = db.query(User).filter_by(user_id=order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #validate product exists
    product = db.query(Product).filter_by(product_id=order.product_id).first()
    if not product: 
        raise HTTPException(status_code=404, detail="Product not found")
    
    #Step 2: create order
    order_id = str(uuid.uuid4())
    db_order = Order(order_id=order_id, **order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.models import models

def get_user_orders(db: Session, user_id: str):
    return db.query(models.Order).filter_by(user_id=user_id).all()

def get_all_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_name(db: Session, product_name: str) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.name.ilike(f"%{product_name}%")).first()

def create_order(db: Session, user_id: str, product_id: str) -> models.Order:
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

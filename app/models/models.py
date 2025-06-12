from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

class Product(Base):
    __tablename__ = "products"
    product_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    product_id = Column(String, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    status = Column(String)

class Conversation(Base):
    __tablename__ = "conversations"
    conv_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    timestamp = Column(String)
    message = Column(String)
    direction = Column(String)  # "in" or "out"

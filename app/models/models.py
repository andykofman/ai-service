from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

#user is a table that stores the users of the system
class User(Base): #SQLAlchemy model (table)
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

#product is a table that stores the products of the users
class Product(Base):
    __tablename__ = "products"
    product_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)

#order is a table that stores the orders of the users
class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))   #this is the foreign key to the user table (one to many relationship)
    product_id = Column(String, ForeignKey("products.product_id")) #this is the foreign key to the product table (one to many relationship)
    quantity = Column(Integer)
    status = Column(String) #pending, shipped, delivered, cancelled

#conversation is a table that stores the conversations of the users
class Conversation(Base):
    __tablename__ = "conversations"
    #conv_id is the id of the conversation
    conv_id = Column(String, primary_key=True, index=True) 
    user_id = Column(String, ForeignKey("users.user_id"))   #this is the foreign key to the user table (one to many relationship)
    timestamp = Column(String)
    message = Column(String)
    direction = Column(String)  # "in" or "out"

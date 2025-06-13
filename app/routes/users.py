from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import User
from app.db.database import get_db
from pydantic import BaseModel
from typing import List

# Pydantic models for request/response
class UserBase(BaseModel):
    user_id: str
    name: str
    email: str

    class Config:
        from_attributes = True  # This enables Pydantic to convert the SQLAlchemy model to a Pydantic model (ORM mode)

class UserCreate(UserBase): #UserCreate (a Pydantic model) which we use for input validation, will implement later
    pass

class UserResponse(UserBase):
    pass

#API Router is used to define the routes for the users
#router is used to define the routes for the users
router = APIRouter()

#create_user is the endpoint that creates a new user
#get_users is the endpoint that returns all the users
@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    #return all the users
    return db.query(User).all()

#create_user is the endpoint that creates a new user

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(user_id=user.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    #create a new user
    db_user = User(**user.model_dump()) #convert/unpacking the pydantic model (user) into a python dictionary
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


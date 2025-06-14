from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Product
from app.db.database import get_db
from pydantic import BaseModel, Field
from typing import List, Literal
import uuid
from pydantic import ConfigDict

router = APIRouter()

class ProductBase(BaseModel):
    name: str
    description: str
    price: int

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: str

#Routes
@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_id = str(uuid.uuid4())
    db_product = Product(product_id=product_id, **product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Product
from app.db.database import get_db
from pydantic import BaseModel, Field
from typing import List, Literal
import uuid
from pydantic import ConfigDict
import logging
from app.config import get_settings

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    try:
        logger.debug("Attempting to create new product")
        logger.debug(f"Product data: {product.model_dump()}")
        
        # Log database connection info (without sensitive data)
        settings = get_settings()
        logger.debug(f"Environment: {settings.ENV}")
        logger.debug(f"Database URL configured: {'Yes' if settings.DATABASE_URL else 'No'}")
        
        product_id = str(uuid.uuid4())
        logger.debug(f"Generated product_id: {product_id}")
        
        db_product = Product(product_id=product_id, **product.model_dump())
        logger.debug("Created Product model instance")
        
        db.add(db_product)
        logger.debug("Added product to session")
        
        try:
            db.commit()
            logger.debug("Successfully committed to database")
        except Exception as commit_error:
            logger.error(f"Database commit error: {str(commit_error)}")
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error while creating product: {str(commit_error)}"
            )
            
        db.refresh(db_product)
        logger.debug("Successfully refreshed product from database")
        return db_product
        
    except Exception as e:
        logger.error(f"Unexpected error in create_product: {str(e)}")
        logger.error(f"Full error details: {repr(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

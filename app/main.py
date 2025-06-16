from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging

from app.config import get_settings
from app.db.database import Base, engine
from app.routes import users_router, orders_router, products_router, webhook_router

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load settings
settings = get_settings()
logger.debug("Settings loaded")

# Create tables in dev
if settings.ENV == "development":
    Base.metadata.create_all(bind=engine)
    logger.debug("Database tables created in development mode")

# App init
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routers
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(products_router)
app.include_router(webhook_router)

# Serve homepage
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

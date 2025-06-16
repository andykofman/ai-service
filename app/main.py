from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging

from app.config import get_settings
from app.db.database import Base, engine
from app.routes import users, orders, products, webhook

# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load settings
settings = get_settings()
logger.debug("Settings loaded")

# DB setup (only in development)
if settings.ENV == "development":
    Base.metadata.create_all(bind=engine)
    logger.debug("Database tables created in development mode")

# FastAPI app init
app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(webhook.router)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

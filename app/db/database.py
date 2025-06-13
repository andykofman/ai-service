from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://user:password@localhost:5432/ai_agent" #this is the url of the database

#connect sqlalchemy to postgres
engine = create_engine(DATABASE_URL)
#SessionLocal is the session to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base is the base class for the models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
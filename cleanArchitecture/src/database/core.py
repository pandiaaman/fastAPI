from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL") # SOMEHOW is giving an error, maybe because of .env not loading properly
DATABASE_URL = "postgresql://username:password@localhost:5432/dbname"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]
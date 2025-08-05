from fastapi import FastAPI

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

# Create a database connection
DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create our app instance - like opening a restaurant
app = FastAPI(title="Todo API", version="1.0.0")

# Database Model - This is how todos are stored in our database
class TodoDB(Base):
    __tablename__ = "todos"  # Name of our table
    
    id = Column(Integer, primary_key=True, index=True)  # Unique identifier
    title = Column(String, index=True)                  # What the todo says
    description = Column(String, nullable=True)         # Optional details
    completed = Column(Boolean, default=False)          # Done or not?
    created_at = Column(DateTime, default=datetime.utcnow)  # When was it made?

# Pydantic Models - These define what data we accept and send via API
class TodoCreate(BaseModel):
    title: str                           # Required field
    description: Optional[str] = None    # Optional field

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows converting from database objects

# Our first route - like the first item on our menu
@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}
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

# Database Model - This is how todos are stored in our database
class TodoDB(Base):
    __tablename__ = "todos"  # Name of our table
    
    id = Column(Integer, primary_key=True, index=True)  # Unique identifier
    title = Column(String, index=True)                  # What the todo says
    description = Column(String, nullable=True)         # Optional details
    completed = Column(Boolean, default=False)          # Done or not?
    created_at = Column(DateTime, default=datetime.utcnow)  # When was it made?

# Create tables
Base.metadata.create_all(bind=engine)

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

# Create our app instance - like opening a restaurant
app = FastAPI(title="Todo API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db  # Give the key to whoever needs it
    finally:
        db.close()  # Always return the key when done

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

@app.get("/todos", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoDB).all()  # Get everything from the todos table
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        # Like saying "Sorry, we don't have a file with that number"
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoDB(
        title=todo.title,
        description=todo.description,
        completed=False,                    # New todos start incomplete
        created_at=datetime.utcnow()       
    )
    db.add(db_todo)        
    db.commit()            
    db.refresh(db_todo)    
    return db_todo






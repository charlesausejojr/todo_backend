# backend/main.py
from fastapi import FastAPI

# Create our app instance - like opening a restaurant
app = FastAPI(title="Todo API", version="1.0.0")

# Our first route - like the first item on our menu
@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}
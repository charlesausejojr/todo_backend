from fastapi import FastAPI

app = FastAPI(title="ToDo API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

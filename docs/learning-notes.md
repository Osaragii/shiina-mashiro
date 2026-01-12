# Week 1: FastAPI Basics

## Day 1: First Endpoint

###What I Built:
- Created my first FastAPI endpoint at "/"
- Returns: {"message": "Hello from Shiina Mashiro"}
- Server runs on http://127.0.0.1.8000

###The Code:
```python
from fastapi import FastAPI

app = FastAPI

@app.get("/")
async def root():
    return {"message": "Hello fro Shiina Mashiro!"}
```

### What I learned:
- FastAPI is the "rope" thagt connects frontend and backend
- @app.get("/") LISTENS for GET requests at the homepage
- When someone visits the URL, FastAPI runs the root() function
- The function returns JSON data back to the browser
- FastAPI auto-generates docs at /docs (cool ahh fr)


### Key Concepts:
- **Decorator (@app.get)**: Registers a function as a route handler
- **GET request**: Asking for information
- **JSON**: Format for sending data {key: value}
- **Endpoint**: A "phone number" the frontend can call

### How to run:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

### What worked:
Server started successfully ✅
Browser showed the JSON message ✅
/docs page appeared automatically ✅

### Adding the /status Endpoint

**Code:**
```python
@app.get("/status")
async def get_status():
    return {
        "status": "operational".
        "version": "0.1.0"
    }
```

**What I Learned:**
- You can have MULTIPLE endpoints in one file
- Each endpoint has its own @app.get() decorator with a different path
- The path ("/status") is what users see in the URL
- The function name (get_status) is just for organization
- FastAPI automatically converts Python dicts to JSON

**Pattern I Noticed:**
```
@app.get("/path")      <- The URL
async def function():  <- Any name you want for the function
    return {....}      <- Data to send back

**Testing:**
- http://127.0.0.1:8000/ → First endpoint
- http://127.0.0.1:8000/status → Second endpoint
- http://127.0.0.1:8000/docs → Shows BOTH endpoints!
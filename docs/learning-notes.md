# Week 1: FastAPI Basics

## Day 1-2: First Endpoint

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
```

**Testing:**
- http://127.0.0.1:8000/ → First endpoint
- http://127.0.0.1:8000/status → Second endpoint
- http://127.0.0.1:8000/docs → Shows BOTH endpoints!

## Day 3: Complex Commands with Parameters

### The Big Idea:
We are learning how to receive COMPLEX commands (action + details) from users, not just simple messages.

### Pizza Analogy
- Simple message: "Pizza" (just one thing)
- Complex command: "Pizza + Large + Pepperoni + Delivery address" (action + details)

### Code structure

**Creating a Command Form:**
```python
class CommandRequest(BaseModel):
    command: str # REQUIRED - What to do
    parameters: dict = {} # OPTIONAL - extra details (default: empty dict)
```

**What This Means:**
- `command` = The action (MUST be provided)
- `parameters` = Extra details (CAN be provided, defaults to `{}` if not)

### Real Examples

**Example 1: Simple command (no extra details)**
```json
{
    "command": "check status:"
}
```
Result: `parameters` automatically becomes `{}`

**Example 2: Command with details**
```json
{
    "command": "open chrome",
    "parameters": {"url": "https://youtube.com"}
}
```
Result: Can access both command and parameters

***Example 3: Complex command**
```json
{
    "command": "send email",
    "parameters": {
        "to": "xyz@example.com",
        "subject": "Meeting",
        "body": "See you tomorrow!"
    }
}
```

### The Complete Flow
```
1. User action (frontend)
   ↓
2. Frontend sends JSON to /execute-command
   ↓
3. FastAPI validates data (Pydantic checks)
   ↓
4. Creates CommandRequest object
   ↓
5. execute_command() functions runs
   ↓
6. Accesses: request.command and request.parameters
   ↓
7. Builds and returns response
   ↓
8. Frontend receives confirmation
```

### Accessing Data in Function
```python
@app.post("/execute-command")
async def execute-command(request: CommandRequest):
    #Access the command
    what_to_do = request.command

    #Access the parameters
    extra_details = request.parameters

    #Access specific parameter
    if "url" in request.parameters:
        url = request.parameters["url"]
    return {
        "status": "success",
        "command": request.command,
        "parameters": request.parameters
    }
```

### Why dict for parameters?

**Problem with fixed fields:**
```python
# BAD - too rigid
class CommandRequest(BaseModel):
    command: str
    url: str # What if command does not need URL?
    recipient: str # What if command does not need recipient?
```

**Solution with dict:**
```python
# GOOD - flexible
class CommandRequest(BaseModel):
    command: str
    parameters: dict = {} # Can hold ANYTHING!
```

Now:
- "open chrome" can have: `{"url": "..."}`
- "send email" can have: `{"to": "...", "subject": "...", "body": "..."}`
- "check status" can have: `{}` (nothing)

### Key Concepts Learned

1. **Optional fields** - Use `= default_value` to make fields optional
2. **Flexible data** - Use `dict` when structure varies
3. **Validation** - Pydantic automatically checks data format
4. **Accessing data** - Use dot notation: `request.command`, `request.parameters`

### Testing
- Use `/docs` interface
- Try commands WITH parameters
- Try commands WITHOUT parameters
- Try INVALID data (missing command) to see validation errors

### What's next
In Week 2, this endpoint will actually eecute commmands (open apps, etc.)
For now, it just validates and acknowledges them.

### Pattern to Remember
```python
# 1. Define what data looks like
class MyModel(BaseModel):
    required_field: str
    optional_field: dict = {}

# 2. Create endpoint that receives it
@app.post("/endpoint")
async def my_function(data: MyModel):
    # 3. Access the data
    value = data.required_field
    extra = data.optional_field

    #4. Return response
    return {"result": "success"}
```
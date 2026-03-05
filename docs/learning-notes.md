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

## Day 4-5: Task Management System

### Task Tracking

**New Data Model:**
```python
from typing import Optional
from datetime import datetime

class TaskResponse(BaseModel):
    task_id: str                    # Unique identifier
    command: str                    # What command was executed
    created_at: str                 # When task was created
    parameters: dict = {}           # Command parameters
    result: Optional[dict] = None   # Result after execution
```

### Task Management Endpoints

**1. List All Tasks:**
```python
GET /tasks
GET /tasks?status=pending # Filter by status
```

**2. Get Specific Task:**
```python
GET /tasks/task_1
```

**3. Cancel Task:**
```python
DELETE /tasks/task_2
```

### Path vs Query Parameters

**Path Parameters** (essential):
```
/tasks/{task_id} ← task_id identifies the resource
Example: /tasks/task_1
```

**Query Parameters** (optional filters):
```
/tasks?status=pending ← status filters results
Example: /tasks?status=completed&limit=10
```

***When to use:**
- Path: Identifying a SPECIFIC resource
- Query: Filtering, sorting, pagnination

---
## Day 6:  Modular Command Execution

### The Big Picture

Instead of one messy file with all commannds, we created a MODULAR system:

```
backend/app/
├── commands/              ← Each category in its own file
│   ├── __init__.py
│   ├── browser.py         ← Browser automation
│   └── desktop.py         ← Desktop control
├── executor.py            ← Routes commands to correct module
└── main.py                ← API endpoints
```

### Why Modular?

**Before (Messy):**
```python
# executor.py with 50+ commands  = nightmare!
def open_browser()...
def screenshot()...
def send_email()...
def search_files()...
# ...50 more - hard to maintain
```

**After (Clean):**
```python
# commands/browser.py - Only browser stuff
def open_browser()...
def search_google()...
def open_youtube()...

# commands/desktop.py - ONLY desktop stuff
def screenshot()...
def open_app()...
def type_text()...
```

### The Executor(Router)

**How it works:**

```python
# executor.py
from commands import browser, desktop

def execute_command(command, parameters):
    command_map = {
        "open_browser": browser.open_browser,
        "screenshot": desktop.take_screenshot,
        # ...more mappings
    }

    if command in command_map:
        return command_map[command](parameters)
```

**Flow:**
```
User sends: {"command": "screenshot"}
    ↓
executor.py receives it
    ↓
Looks up "screenshot" in command_map
    ↓
Calls: desktop.take_screenshot()
    ↓
Returns result
```

### Available commands (6 Total)

**Browser (commands/browser.py):**
1. `open_browser` - Open any URL
2. `search_google` - Google Search
3. `open_youtube` - YouTube (with optional search)

**Desktop (commands/desktop.py):**
4. `screenshot` - Take screenshot
5. `open_app` - Open applications(notepad, chrome, calculator)
6. `type_text` - Type text automatically

### How to Add New Commands

**Step 1:** Add function to appropriate module
```python
# commands/browser.py
def close_browser():
    #implementation
    return {"success": True}
```

**Step 2:** Register in executor
```python
# executor.py
command_map = {
    # ...existing commands
    "clean_browser": browser.close_browser, # NEW
}
```

## Day 7: Configuration Management

### The Problem: Hardcoded Values

**Before (Bad):**
```python
# Hardcoded everywhere!
screenshots_dir = Path("screenshot")
default_url = "https://google.com"
log_level = "INFO"
```

**Issues:**
- Cannot customize without editing code
- Different settings for dev/prod means editing files
- Secrets (API keys) exposed in code
- Hard to change behaviour

### The Solution: configuration System

**1. `.env` (User Settings - NOT in git)**
```env
# User can customize these!
SCREENSHOTS_DIR=screenshots
DEFAULT_BROWSER_URL=https://google.com
LOG_LEVEL=INFO
ENVIRONMENT=development
```

**2. `.env.example` (Template - IN git)**
```env
# Same as .env but without secrets
# Other developers copy this to create their .env
```

**3. `config.py` (Loads settings)**
```python
from dotenv import load_dotenv
import os

class Config:
    SCREENSHOTS_DIR = Path(os.getenv("SCREENSHOTS_DIR", "screenshots"))
    DEFAULT_BROWSER_URL = os.getenv(DEFAULT_BROWSER_URL, "https://google.com")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

### How it works

**Step 1:** User creates `.env` with custom settings
```env
SCREENSHOTS_DIR=C:/Users/Me/Pictures/Shiina
DEFAULT_BROWSER_URL=https://github.com
```

**Step 2:** Config loads these on startup
```python
from config import config

# config.SCREENSHOTS_DIR is now C:/Users/Me/Pictures/Shiina
```

**Step 3:** Code uses config instead of hardcoded values
```python
# Before
screenshots_dir = Path("screenshots") # Hardcoded!

# After
from ..config import config
screenshots_dir = config.SCREENSHOTS_DIR # From .env
```

### Key Concepts

**1. Environment Variables:**
- Settings stored outside code
- Different per environment (dev/staging/prod)
- Secrets stay secret

**2. python-dotenv:**
```python
from dotenv import load_dotenv
load_dotenv() # Loads .env file into environment
```

**3. Default Values:**
```python
os.getenv("KEY", "default")
# If KEY not in .env, use "default"
```

**4. Type Conversion:**
```python
# String to boolean
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() == "true"

# String to path
SCREENSHOTS_DIR = PAth(os.getenv("SCREENSHOTS_DIR", "screenshots"))

# String to int
MAX_TASLS = int(os.getenv("MAX_TASKS", "100"))
```

### Relative Imports (Important!)

**The `..` syntax:**
```python
# In commands/browser.py
from ..config import config
# ↑↑
# Two dots = go up one directory level
```

**Directory Structure:**
```
app/
├── config.py              ← Config is here
└── commands/
    └── browser.py         ← We are here
```

**From `commands/browser.py:`
- `.config` = same level (commands/config.py - does not exist!)
- `..config` = up one level (app/config.py - correct!)

### gitignore Update

**Added to `.gitignore`:**
```
# Don't commit these!
.env               # User secrets
logs/              # Log files
screenshots/       # User data
```

---

## Day 8

### Professional Development Setup

**Added 3 tools:**

**1. Black(Code Formatter):**
- Automatically formats code to PEP 8 style
- No more arguing about formatting
- Consistent style across project

**2. Ruff (Linter):**
- Fast Python Linter
- Catches syntax errors
- Auto-sorts imports
- Enforces best practices

**3. Pre-commit Hooks:**
- Runs Black + Ruff BEFORE every commit
- Prevents bad code form entering repo
- Automatic quality control

**Configuration (`.pre-commit-config.yaml`):**
```yaml
  - repos: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [ --fix ]
    -repo: https://github.com/psf/black
     rev: 23.12.1
     hooks:
       -id: black
```

## Summary: What I have Built

### API Endpoints (6):
1. `GET /` - Health check
2. `GET /status` - System status
3. `POST /execute-command` - Execute commands
4. `GET /tasks` - List tasks
5. `GET /tasks/{task_id}` - Get specific task
6. `DELETE /tasks/{task_id}` - Cancel task

### Command System:
- Modular architecture (browser + desktop modules)
- Central executor/router
- 6 working commands
- Easy to expand

### Infrastructure:
- Configuration management (.env + config.py)
- Task tracking system
- Code quality tools (Black, Ruff, pre-commit)
- Professional project structure

### Key Learnings:
-  FastAPI basics (decorators, routes, responses)
- Pydantic validation
- Modular Architecture
- Configuration management
- Relative imports
- Path vs Query parameters
- Professional dev practices

---
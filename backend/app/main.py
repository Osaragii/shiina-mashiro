from fastapi import FastAPI    # For building the API
from pydantic import BaseModel # Used for data validation
from typing import Optional # For optional fields
from datetime import datetime # For timestamps

# Create FastAPI application instance with metadata
app = FastAPI(
    title="Shiina Mashiro API",
    description="AI-powered desktop asssitant backend",
    version="0.1.0"
)

# ============================================================================
# DATA MODELS (Pydantic)
# ============================================================================
# These define the structure of data we expect to receive in requests

# Define what data we expect to receive, here its for text messages
class Message(BaseModel):
    text: str

# Model for command execution requests, defines the structure of commands sent from the frontend to be executed by the assistant
class CommandRequest(BaseModel):
    command: str
    parameters: dict = {} # Optional field with default value

# Model for task responses - tracks command execution status
class TaskResponse(BaseModel):
    task_id: str                    #Unique identifier for the task
    command: str                    # What command was executed
    status: str                     # "pending", "running", "completed", "failed"
    created_at: str                 # When task was created
    parameters: dict = {}           # Command parameters
    result: Optional[dict] = None   # Result after execution (None if not done)

# ============================================================================
# IN-MEMORY TASK STORAGE
# ============================================================================
# Temporary storage for tasks (will use Redis/database later in production)

tasks = {}          # Dictionary to store all tasks
task_counter = 0    # Counter for generating unique task IDs

# ============================================================================
# API ENDPOINTS
# ============================================================================

# Confirs the API is running
@app.get("/")
async def root():
    return {"message": "Hi! I'm Shiina Mashiro, your personal assistant!",
            "status": "ready"
    }

# Returns operational status and version info
@app.get("/status")
async def get_status():
    return {
        "status": "operational",
        "version": "0.1.0"
    }

# Executes a command from the user and creates a task to track it
@app.post("/execute-command")
async def execute_command(request: CommandRequest):
    global task_counter

    # Generate unique task id
    task_counter += 1
    task_id = f"task_{task_counter}"

    # Create task object
    task = {
        "task_id": task_id,
        "command": request.command,
        "parameters": request.parameters,
        "status": "pending", # Will be "running" when executing and "completed" when done
        "created_at": datetime.now().isoformat(),
        "result": None
    }

    # Store task in memory
    tasks[task_id] = task
    return {
        "status": "queued",
        "task_id": task_id,
        "message": f"Got it! I'll '{request.command}' for you right away"
    }
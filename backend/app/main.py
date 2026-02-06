from fastapi import FastAPI  # For building the API
from pydantic import BaseModel  # Used for data validation
from typing import Optional  # For optional fields
from datetime import datetime  # For timestamps

# Create FastAPI application instance with metadata
app = FastAPI(
    title="Shiina Mashiro API",
    description="AI-powered desktop asssitant backend",
    version="0.1.0",
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
    parameters: dict = {}  # Optional field with default value


# Model for task responses - tracks command execution status
class TaskResponse(BaseModel):
    task_id: str  # Unique identifier for the task
    command: str  # What command was executed
    status: str  # "pending", "running", "completed", "failed"
    created_at: str  # When task was created
    parameters: dict = {}  # Command parameters
    result: Optional[dict] = None  # Result after execution (None if not done)


# ============================================================================
# IN-MEMORY TASK STORAGE
# ============================================================================
# Temporary storage for tasks (will use Redis/database later in production)

tasks = {}  # Dictionary to store all tasks
task_counter = 0  # Counter for generating unique task IDs

# ============================================================================
# API ENDPOINTS
# ============================================================================


# Confirs the API is running
@app.get("/")
async def root():
    return {
        "message": "Hi! I'm Shiina Mashiro, your personal assistant!",
        "status": "ready",
    }


# Returns operational status and version info
@app.get("/status")
async def get_status():
    return {"status": "operational", "version": "0.1.0"}


# List all tasks, optionally filtered by status
@app.get("/tasks")
async def list_tasks(status: Optional[str] = None):
    if status:
        # Filter by status if provided
        filtered = {k: v for k, v in tasks.items() if v["status"] == status}
        return {"tasks": list(filtered.values()), "count": len(filtered)}

    # Return all tasks
    return {"tasks": list(tasks.values()), "count": len(tasks)}


# Get status of a specific task
@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    if task_id not in tasks:
        return {"error": "Task not found", "task_id": task_id}

    return tasks[task_id]


# Cancel a pending task
@app.delete("/tasks/{task_id}")
async def cancel_task(task_id: str):
    if task_id not in tasks:
        return {"error": "Task not found"}

    if tasks[task_id]["status"] == "completed":
        return {"error": "Cannot cancel completed task"}

    tasks[task_id]["status"] = "cancelled"
    return {"message": "Task cancelled", "task_id": task_id}


# Executes a command from the user and creates a task to track it
@app.post("/execute-command")
async def execute_command_endpoint(request: CommandRequest):
    global task_counter

    # Generate unique task id
    task_counter += 1
    task_id = f"task_{task_counter}"

    # Create task object
    task = {
        "task_id": task_id,
        "command": request.command,
        "parameters": request.parameters,
        "status": "running",  # Will be "running" when executing and "completed" when done
        "created_at": datetime.now().isoformat(),
        "result": None,
    }

    # Store task in memory
    tasks[task_id] = task

    # Executes the command
    from .executor import execute_command

    execution_result = execute_command(request.command, request.parameters)

    # Update task with result
    tasks[task_id]["result"] = execution_result
    tasks[task_id]["status"] = (
        "completed" if execution_result.get("success") else "failed"
    )

    return {
        "status": "completed" if execution_result.get("success") else "failed",
        "task_id": task_id,
        "message": f"Got it! I'll '{request.command}' for you right away",
        "result": execution_result,
    }

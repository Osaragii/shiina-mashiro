from fastapi import FastAPI    # For building the API
from pydantic import BaseModel # Used for data validation

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


# ============================================================================
# API ENDPOINTS
# ============================================================================

# Confirs the API is running
@app.get("/")
async def root():
    return {"message": "Hello from Shiina Mashiro!"}

# Returns operational status and version info
@app.get("/status")
async def get_status():
    return {
        "status": "operational",
        "version": "0.1.0"
    }

# Receives a message and sends it back with confirmation, mainly for testing POST requests and data validation
@app.post("/echo")
async def echo_message(message: Message):
    return {
        "you_said": message.text,
        "response": f"I heard you say: {message.text}"
    }

# Executes a command from the user, main endpoint for the assistant
@app.post("/execute-command")
async def execute_command(request: CommandRequest):
    return {
        "status": "success",
        "command": request.command,
        "parameters": request.parameters,
        "message": f"Command '{request.command}' received and queued for execution"
    }
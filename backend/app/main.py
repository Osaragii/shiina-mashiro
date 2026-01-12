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
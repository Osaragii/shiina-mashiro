from fastapi import FastAPI

app = FastAPI(
    title="Shiina Mashiro API",
    description="AI-powered desktop asssitant backend",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Hello from Shiina Mashiro!"}

@app.get("/status")
async def get_status():
    return {
        "status": "operational",
        "version": "0.1.0"
    }
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routes import webhook, notes

app = FastAPI(
    title="DevLog AI",
    description="Personal Developer Activity Aggregator and Content Generator",
    version="1.0 MVP"
)

# Enable CORS for local single-user frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(webhook.router)
app.include_router(notes.router)

@app.get("/health")
def health_check():
    """
    Check backend status.
    Returns:
        JSON response with health status.
    """
    return {
        "success": True,
        "data": {
            "status": "healthy"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

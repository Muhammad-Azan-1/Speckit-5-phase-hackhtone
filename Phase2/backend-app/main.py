from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes.setup import router as setup_router
from routes.tasks import router as tasks_router
from routes.dashboard import router as dashboard_router
from routes.categories import router as categories_router
from routes.user import router as user_router
from db import create_db_and_tables
from contextlib import asynccontextmanager
from rate_limit_general import APIRateLimitMiddleware

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield
    # Cleanup on shutdown if needed

# Create FastAPI app instance
app = FastAPI(
    title="Todo API - Backend Development Environment",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiting middleware
app.add_middleware(APIRateLimitMiddleware)

# Configure CORS middleware (Must be adding LAST to be the OUTERMOST middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Auth is handled via dependency injection in routes (get_current_user)

# Include setup, task, dashboard, and category routes
app.include_router(setup_router)
app.include_router(tasks_router)
app.include_router(dashboard_router)
app.include_router(categories_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Todo API Backend is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint - returns the health status of the backend service"""
    return {
        "status": "healthy",
        "timestamp": "2026-01-07T08:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
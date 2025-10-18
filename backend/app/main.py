from fastapi import FastAPI
from app.routes import query_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="AI Research Assistant API",
    description="AI-powered research assistant with LangChain integration",
    version="1.0.0"
)

# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Research Assistant API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-research-assistant-backend",
        "version": "1.0.0"
    }

app.include_router(query_router.router, prefix="/api")

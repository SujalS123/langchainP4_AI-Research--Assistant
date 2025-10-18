"""
Simple FastAPI server that bypasses Pydantic issues.
Provides the search functionality with minimal dependencies.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import uvicorn

# Import our working search function
from app.services.langchain_service import perform_web_search

app = FastAPI(title="Simple AI Research Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimpleQueryRequest(BaseModel):
    query: str
    options: dict = {}

@app.get("/")
async def root():
    return {"message": "Simple AI Research Assistant API"}

@app.post("/api/query")
async def query_research(request: SimpleQueryRequest):
    try:
        # Perform the search
        search_results = perform_web_search(request.query)
        
        # Return the response in the expected format
        return {
            "status": "ok",
            "summary": search_results,
            "query": request.query,
            "tools_available": ["Search", "Calculator"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting Simple AI Research Assistant Server...")
    print("Server will be available at: http://localhost:8000")
    print("API endpoint: http://localhost:8000/api/query")
    uvicorn.run(app, host="0.0.0.0", port=8000)

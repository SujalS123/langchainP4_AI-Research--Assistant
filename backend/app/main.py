from fastapi import FastAPI
from app.routes import query_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Research Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router.router, prefix="/api")

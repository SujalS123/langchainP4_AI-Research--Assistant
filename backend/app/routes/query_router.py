from fastapi import APIRouter, HTTPException
from app.models.request_models import QueryRequest
from app.services.langchain_service import run_agent

router = APIRouter()

@router.post("/query")
async def query_research(req: QueryRequest):
    try:
        response = await run_agent(req.query, req.options)
        return {"status": "ok", **response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

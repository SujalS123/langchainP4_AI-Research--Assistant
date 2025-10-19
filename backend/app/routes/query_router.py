from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.request_models import QueryRequest
from app.services.langchain_service import run_agent

router = APIRouter()

@router.options("/query")
async def options_query():
    response = JSONResponse(content={"status": "ok"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@router.post("/query")
async def query_research(req: QueryRequest):
    try:
        response = await run_agent(req.query, req.options)
        result = {"status": "ok", **response}
        json_response = JSONResponse(content=result)
        json_response.headers["Access-Control-Allow-Origin"] = "*"
        return json_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

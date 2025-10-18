from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    options: dict = {}

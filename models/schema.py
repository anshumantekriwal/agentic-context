from pydantic import BaseModel, Field
from typing import List, Optional

class APIKey(BaseModel):
    api_key: str = Field(..., min_length=10, max_length=10, pattern="^[a-zA-Z0-9]{10}$")

class UploadResponse(BaseModel):
    agent_id: str
    filename: str
    chunk_count: int

class QueryRequest(BaseModel):
    query: str
    agent_id: str

class QueryResponse(BaseModel):
    answer: str
    source_chunks: List[str]

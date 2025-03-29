from pydantic import BaseModel, Field
from typing import List, Optional

class UploadResponse(BaseModel):
    agent_id: str
    filename: str
    chunk_count: int

class RetrieveRequest(BaseModel):
    query: str
    agent_id: str
    top_k: int = Field(default=5, ge=1, le=20)

class RetrieveResponse(BaseModel):
    chunks: List[str]
    metadata: Optional[List[dict]] = None

class FormatRequest(BaseModel):
    chunks: List[str]

class FormatResponse(BaseModel):
    formatted_context: str

class QueryRequest(BaseModel):
    query: str
    agent_id: str

class QueryResponse(BaseModel):
    answer: str
    source_chunks: List[str]

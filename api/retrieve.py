from fastapi import APIRouter, HTTPException
from models.schema import RetrieveRequest, RetrieveResponse
from services.chroma_service import ChromaService

router = APIRouter()

@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_chunks(request: RetrieveRequest) -> RetrieveResponse:
    """
    Retrieve relevant document chunks based on a query
    
    This endpoint:
    1. Takes a query and document ID
    2. Searches ChromaDB using MMR retrieval
    3. Returns top k most relevant chunks with metadata
    """
    try:
        chroma_service = ChromaService()
        chunks, metadata = chroma_service.search(
            query=request.query,
            agent_id=request.agent_id,
            top_k=request.top_k
        )
        
        return RetrieveResponse(
            chunks=chunks,
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chunks: {str(e)}"
        )

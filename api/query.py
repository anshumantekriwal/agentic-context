from fastapi import APIRouter, HTTPException
from models.schema import QueryRequest, QueryResponse, RetrieveRequest, FormatRequest
from services.chroma_service import ChromaService
from services.deepseek_service import DeepSeekService

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest) -> QueryResponse:
    """
    Process a user query with RAG
    
    This endpoint:
    1. Retrieves relevant chunks from ChromaDB
    2. Formats the chunks using DeepSeek
    3. Generates a final answer using the formatted context
    """
    try:
        # Get relevant chunks
        chroma_service = ChromaService()
        chunks, _ = chroma_service.search(
            query=request.query,
            agent_id=request.agent_id,
        )
        
        # Format chunks
        deepseek_service = DeepSeekService()
        formatted_context = deepseek_service.format_context(chunks)
        

        
        return QueryResponse(
            answer=formatted_context,
            source_chunks=chunks,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

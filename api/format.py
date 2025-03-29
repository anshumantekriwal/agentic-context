from fastapi import APIRouter, HTTPException
from models.schema import FormatRequest, FormatResponse
from services.deepseek_service import DeepSeekService

router = APIRouter()

@router.post("/format", response_model=FormatResponse)
async def format_chunks(request: FormatRequest) -> FormatResponse:
    """
    Format and structure raw chunks using DeepSeek
    
    This endpoint:
    1. Takes a list of raw text chunks
    2. Sends them to DeepSeek for formatting
    3. Returns cleaned and structured context
    """
    try:
        deepseek_service = DeepSeekService()
        formatted_context = deepseek_service.format_context(request.chunks)
        
        return FormatResponse(
            formatted_context=formatted_context
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error formatting chunks: {str(e)}"
        )

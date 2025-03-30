from fastapi import Request, HTTPException
from dotenv import load_dotenv
import os

async def verify_api_key(request: Request):
    load_dotenv()
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        ) 
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from api import upload, query
from middleware.auth import verify_api_key
from models.schema import UploadResponse, QueryRequest, QueryResponse
from dotenv import load_dotenv
import os



app = FastAPI(
    title="Xade Agentic Context",
    description="RAG System with DeepSeek and ChromaDB",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(query.router, prefix="/api/v1", tags=["Query"])

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "RAG system is running"}

if __name__ == "__main__":
    import uvicorn
    from langfuse import Langfuse
    load_dotenv()

    langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host="https://us.cloud.langfuse.com"
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)

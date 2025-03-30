from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from api import upload, query
from middleware.auth import verify_api_key
from models.schema import UploadResponse, QueryRequest, QueryResponse

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

@app.post("/upload", response_model=UploadResponse)
async def upload_document(request: Request, _: None = Depends(verify_api_key)):
    # Your existing upload logic here
    pass

@app.post("/query", response_model=QueryResponse)
async def query_document(request: Request, query: QueryRequest, _: None = Depends(verify_api_key)):
    # Your existing query logic here
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import upload, retrieve, format, query

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
app.include_router(retrieve.router, prefix="/api/v1", tags=["Retrieve"])
app.include_router(format.router, prefix="/api/v1", tags=["Format"])
app.include_router(query.router, prefix="/api/v1", tags=["Query"])

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "RAG system is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

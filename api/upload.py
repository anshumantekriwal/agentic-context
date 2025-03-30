from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from uuid import uuid4
import os
from typing import List
import shutil
from middleware.auth import verify_api_key
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from services.chroma_service import ChromaService
from models.schema import UploadResponse

router = APIRouter()
UPLOAD_DIR = "./uploads"
ALLOWED_EXTENSIONS = {".pdf", ".txt"}

def validate_file(file: UploadFile) -> str:
    """Validate file type and extension"""
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return file_ext

def save_file(file: UploadFile, agent_id: str, name: str) -> str:
    """Save uploaded file and return file path"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"agent_{agent_id}-{name}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

def load_document(file_path: str) -> Document:
    """Load document based on file type"""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == ".pdf":
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        text = " ".join(map(lambda x: x.page_content, documents))
    else:  # .txt
        loader = TextLoader(file_path)
        documents = loader.load()
        text = documents[0].page_content
        
    return Document(page_content=text)

def split_document(document: Document) -> List[Document]:
    """Split document into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=0,
        add_start_index=True
    )
    return splitter.split_documents([document])

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...), agent_id: str = Form(...), _: None = Depends(verify_api_key)) -> UploadResponse:
    """
    Upload and process a document file (PDF or TXT)
    
    This endpoint:
    1. Validates the file type
    2. Saves the file
    3. Processes the document
    4. Stores chunks in ChromaDB
    5. Returns a document ID for future queries
    """
    try:
        # Validate file
        validate_file(file)

        name = file.filename

        # Save file
        file_path = save_file(file, agent_id, name=str(name))
        
        # Process document
        document = load_document(file_path)
        chunks = split_document(document)
        
        # Generate document ID        
        # Store in ChromaDB
        chroma_service = ChromaService()
        chroma_service.add_chunks(chunks, agent_id)
        
        return UploadResponse(
            agent_id=agent_id,
            filename=file.filename,
            chunk_count=len(chunks)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

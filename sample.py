"""
RAG System with DeepSeek and ChromaDB

This script implements a Retrieval-Augmented Generation (RAG) system using ChromaDB 
as the vector store and DeepSeek for text generation.
"""

# Core dependencies
import os
from uuid import uuid4
from typing import List
from dotenv import load_dotenv

# OpenAI and DeepSeek
import openai
from openai import OpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Document processing
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Vector store and embeddings
import chromadb
from langchain_chroma import Chroma

# Prompts and templates
from langchain_core.prompts import ChatPromptTemplate

# Constants
PDF_PATH = "./uploads/ISLP.pdf"
CHROMA_DIR = "./chromadb"
CHUNK_SIZE = 4000
CHUNK_OVERLAP = 0
AGENT_ID = "islp"


def init_models():
    """Initialize AI models and clients."""
    load_dotenv()
    
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    return model, client


def load_document(path: str) -> Document:
    """
    Load and process a PDF document.
    
    Args:
        path: Path to the PDF file
        
    Returns:
        Document: Processed document object
    """
    loader = PyMuPDFLoader(path)
    documents = loader.load()
    text = str(' '.join(map(lambda x: x.page_content, documents)))
    return Document(page_content=text)


def split_document(document: Document) -> List[Document]:
    """
    Split document into chunks for processing.
    
    Args:
        document: Input document to split
        
    Returns:
        List[Document]: List of document chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True
    )
    return splitter.split_documents([document])


def init_vector_store(chunks: List[Document], agent_id: str) -> Chroma:
    """
    Initialize and populate ChromaDB vector store.
    
    Args:
        chunks: Document chunks to store
        
    Returns:
        Chroma: Initialized vector store
    """
    vector_store = Chroma(
        collection_name=agent_id,
        embedding_function=OpenAIEmbeddings(model='text-embedding-3-small'),
        persist_directory=CHROMA_DIR,
        create_collection_if_not_exists=True
    )

    # Check for existing documents
    existing_docs = vector_store.similarity_search("", k=1)

    if not existing_docs:
        uuids = [str(uuid4()) for _ in range(len(chunks))]
        vector_store.add_documents(documents=chunks, ids=uuids)
        print("Documents added to vector store")
    else:
        print("Documents already exist in vector store")

    return vector_store


def create_retriever(vector_store: Chroma):
    """
    Create a retriever with MMR search configuration.
    
    Args:
        vector_store: Initialized vector store
        
    Returns:
        Retriever object
    """
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 10,
            "lambda_mult": 0.25
        }
    )


def get_prompt_template() -> ChatPromptTemplate:
    """
    Create the formatting assistant prompt template.
    
    Returns:
        ChatPromptTemplate: Configured prompt template
    """
    prompt_text = '''
    You are a formatting and organization assistant.

    Your job is to take the raw information retrieved by a RAG system (provided below) 
    and process it to create a clear, well-structured, and logically ordered context. 
    This context will be used by another model to answer a user query, so you must not 
    answer the query yourself.

    Instructions:
    - Organize the information into sections or bullet points.
    - Remove duplicates and irrelevant or conflicting data.
    - Preserve technical or factual accuracy.
    - Do not fabricate or infer missing information.
    - Make the result easy for another model to read and use as direct context.
    - Ensure all the information from the retrieved chunks is present

    Below is the raw retrieved data:
    ---
    {retrieved_chunks_here}
    ---

    Return only the cleaned and structured context below.

    Context:
    '''

    return ChatPromptTemplate.from_messages([("system", prompt_text)])


def query_system(query: str, retriever, client: OpenAI):
    """
    Query the RAG system with user input.
    
    Args:
        query: User query string
        retriever: Configured retriever
        client: OpenAI client
        
    Returns:
        str: Generated response
    """
    retrieved_chunks = retriever.invoke(query)
    prompt = get_prompt_template().format(retrieved_chunks_here=retrieved_chunks)
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": prompt}],
        stream=False
    )
    
    return response.choices[0].message.content


def main():
    """Main execution function."""
    # Initialize models and clients
    print("Initializing models and clients...")
    model, client = init_models()
    
    # Load and process document
    print("\nLoading and processing document...")
    document = load_document(PDF_PATH)
    chunks = split_document(document)
    
    # Initialize vector store and retriever
    print("\nSetting up vector store and retriever...")
    vector_store = init_vector_store(chunks, f"agent_{AGENT_ID}")
    retriever = create_retriever(vector_store)
    
    # Example query
    print("\nExecuting example query...")
    query = "What are RNNs?"
    result = query_system(query, retriever, client)
    print(f"\nQuery: {query}\nResult:\n{result}")

if __name__ == "__main__":
    main()

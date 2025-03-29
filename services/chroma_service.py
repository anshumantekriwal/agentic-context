from typing import List, Tuple
from uuid import uuid4
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

class ChromaService:
    def __init__(self):
        load_dotenv()
        self.persist_directory = "./chromadb"
        self.embedding_function = OpenAIEmbeddings(model='text-embedding-3-small')
        self.chunk_size = 4000
        self.chunk_overlap = 0

    def _get_collection(self, agent_id: str) -> Chroma:
        """Get or create a ChromaDB collection for the document"""
        return Chroma(
            collection_name=f"agent_{agent_id}",
            embedding_function=self.embedding_function,
            persist_directory=self.persist_directory,
            collection_metadata={"agent_id": agent_id},
            create_collection_if_not_exists=True
        )

    def add_chunks(self, chunks: List[Document], agent_id: str) -> None:
        """Add document chunks to ChromaDB"""
        vector_store = self._get_collection(agent_id)
        
        # Generate UUIDs for each chunk
        ids = [str(uuid4()) for _ in range(len(chunks))]
        
        # Add documents with metadata
        for idx, chunk in enumerate(chunks):
            if not hasattr(chunk, 'metadata'):
                chunk.metadata = {}
            chunk.metadata.update({
                'agent_id': agent_id,
                'chunk_index': idx,
                'start_index': chunk.metadata.get('start_index', 0)
            })
        
        # Add to vector store
        vector_store.add_documents(
            documents=chunks,
            ids=ids
        )

    def search(
        self,
        query: str,
        agent_id: str,
        top_k: int = 5,
        search_type: str = "mmr"
    ) -> Tuple[List[str], List[dict]]:
        """
        Search for relevant chunks using MMR or similarity search
        
        Args:
            query: Search query
            agent_id: Document ID to search in
            top_k: Number of results to return
            search_type: "mmr" or "similarity"
            
        Returns:
            Tuple of (chunks, metadata)
        """
        vector_store = self._get_collection(agent_id)
        
        search_kwargs = {
            "k": top_k,
        }
        
        if search_type == "mmr":
            search_kwargs.update({
                "fetch_k": min(10, top_k * 2),
                "lambda_mult": 0.25
            })
            
        retriever = vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
        
        # Get results
        results = retriever.invoke(query)
        
        # Extract chunks and metadata
        chunks = [doc.page_content for doc in results]
        metadata = [doc.metadata for doc in results]
        
        return chunks, metadata

    def delete_collection(self, agent_id: str) -> None:
        """Delete a document collection"""
        vector_store = self._get_collection(agent_id)
        vector_store.delete_collection()

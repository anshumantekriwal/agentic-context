import os
from typing import List, Tuple
from openai import OpenAI

class DeepSeekService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.model = "deepseek-chat"

    def format_context(self, chunks: List[str]) -> str:
        """
        Format and structure retrieved chunks using DeepSeek
        
        Args:
            chunks: List of raw text chunks from ChromaDB
            
        Returns:
            str: Cleaned and structured context
        """
        prompt = self._get_formatting_prompt(chunks)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],
        )
        
        return response.choices[0].message.content

    def _get_formatting_prompt(self, chunks: List[str]) -> str:
        """Create the formatting prompt"""
        return f'''
You are a formatting and organization assistant.

Your job is to take the raw information retrieved by a RAG system (provided below) 
and process it to create a clear, well-structured, and logically ordered context.
This context will be used by another model to answer a user query, so you must not 
answer the query yourself.

Instructions:
- Organize the information into sections or bullet points
- Remove duplicates and irrelevant or conflicting data
- Preserve technical or factual accuracy
- Do not fabricate or infer missing information
- Make the result easy for another model to read and use as direct context
- Ensure all the important information from the retrieved chunks is present

Below is the raw retrieved data:
---
{chr(10).join(chunks)}
---

Return only the cleaned and structured context below.

Context:'''



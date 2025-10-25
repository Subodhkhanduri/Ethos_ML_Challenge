"""
RAG Retriever - Query FAISS indices for relevant examples
"""

import faiss
import json
from sentence_transformers import SentenceTransformer
from typing import List, Dict


class RAGRetriever:
    """Retrieve relevant examples from FAISS knowledge base"""
    
    def __init__(self, knowledge_base_path: str):
        self.kb_path = knowledge_base_path
        self.encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Load FAISS indices
        self.decomp_index = faiss.read_index(f"{knowledge_base_path}/decomp_index.faiss")
        self.tools_index = faiss.read_index(f"{knowledge_base_path}/tools_index.faiss")
        
        # Load chunks from the correct .txt files
        with open(f"{knowledge_base_path}/kb_decomposition_examples.txt", "r") as f:
            self.decomp_chunks = [line.strip() for line in f if line.strip()]

        with open(f"{knowledge_base_path}/kb_tool_syntax_examples.txt", "r") as f:
            self.tool_chunks = [line.strip() for line in f if line.strip()]

        
        print("✓ RAG retriever initialized")
    
    def retrieve_decomposition_examples(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve relevant problem decomposition examples"""
        query_embedding = self.encoder.encode([query])
        distances, indices = self.decomp_index.search(query_embedding, top_k)
        
        examples = [self.decomp_chunks[idx] for idx in indices[0]]
        return examples
    
    def retrieve_tool_examples(self, query: str, top_k: int = 2) -> List[str]:
        """Retrieve relevant tool usage examples"""
        query_embedding = self.encoder.encode([query])
        distances, indices = self.tools_index.search(query_embedding, top_k)
        
        examples = [self.tool_chunks[idx] for idx in indices[0]]
        return examples

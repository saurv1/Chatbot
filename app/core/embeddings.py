"""
Embedding model management for the chatbot tutor
"""
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            List of embedding values
        """
        return self.model.encode(text).tolist()
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding lists
        """
        return self.model.encode(texts).tolist()
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings
        
        Returns:
            Embedding dimension
        """
        # Create a dummy embedding to get dimension
        dummy_embedding = self.embed_text("test")
        return len(dummy_embedding)
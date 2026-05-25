"""
RAG (Retrieval Augmented Generation) implementation - Updated for ChromaDB v0.4+
"""
import os
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

try:
    from .embeddings import EmbeddingModel
except ImportError:
    from .embeddings_simple import SimpleEmbeddingModel as EmbeddingModel

class RAGSystem:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize RAG system with ChromaDB - Updated for new ChromaDB API
        """
        self.persist_directory = persist_directory
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with new API
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="tutor_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embedding model
        self.embedding_model = EmbeddingModel()
    
    def add_documents(self, documents: List[str], metadatas: List[Dict] = None):
        """
        Add documents to the vector database
        """
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        # Generate IDs
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Add to collection - ChromaDB now handles embeddings automatically
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def retrieve_relevant_documents(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Retrieve relevant documents for a query
        """
        # Query the collection - ChromaDB handles embeddings automatically
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        retrieved_docs = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                retrieved_docs.append({
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else 0.0
                })
        
        return retrieved_docs
    
    def load_sample_documents(self, data_dir: str = "./data/sample_documents"):
        """
        Load sample documents from directory
        """
        documents = []
        metadatas = []
        
        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                if filename.endswith('.txt'):
                    filepath = os.path.join(data_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            documents.append(content)
                            metadatas.append({"source": filename})
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
        
        if documents:
            self.add_documents(documents, metadatas)
            print(f"✅ Loaded {len(documents)} sample documents into ChromaDB")
        else:
            print("❌ No sample documents found. Creating default documents...")
            self._create_default_documents()
    
    def _create_default_documents(self):
        """Create default documents if none exist"""
        default_docs = [
            "Mathematics is the study of numbers and patterns. Basic operations include addition, subtraction, multiplication, and division.",
            "Physics studies matter, energy, and forces. Newton's laws describe how objects move.",
            "Programming involves writing instructions for computers. Variables store data and functions perform tasks."
        ]
        
        default_metadatas = [
            {"source": "default_math"}, 
            {"source": "default_physics"}, 
            {"source": "default_programming"}
        ]
        
        self.add_documents(default_docs, default_metadatas)
        print("✅ Created default documents")
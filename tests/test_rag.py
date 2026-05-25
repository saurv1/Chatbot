"""
Tests for RAG functionality
"""
import unittest
import os
import tempfile
from app.core.rag import RAGSystem
from app.core.embeddings import EmbeddingModel

class TestRAGSystem(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.rag_system = RAGSystem(persist_directory=self.temp_dir)
        self.embedder = EmbeddingModel()
    
    def tearDown(self):
        """Clean up after tests"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_embedding_generation(self):
        """Test embedding model functionality"""
        text = "Test sentence for embedding"
        embedding = self.embedder.embed_text(text)
        
        self.assertIsInstance(embedding, list)
        self.assertTrue(len(embedding) > 0)
        self.assertIsInstance(embedding[0], float)
    
    def test_document_addition(self):
        """Test adding documents to RAG system"""
        documents = [
            "This is a test document about mathematics.",
            "This is another document about physics."
        ]
        
        self.rag_system.add_documents(documents)
        
        # Test retrieval
        results = self.rag_system.retrieve_relevant_documents("mathematics", n_results=1)
        self.assertEqual(len(results), 1)
        self.assertIn("mathematics", results[0]['document'].lower())
    
    def test_document_retrieval(self):
        """Test document retrieval functionality"""
        documents = [
            "Python is a programming language known for its simplicity.",
            "JavaScript is used for web development and interactive websites.",
            "Machine learning involves training algorithms on data."
        ]
        
        self.rag_system.add_documents(documents)
        
        # Test relevant retrieval
        results = self.rag_system.retrieve_relevant_documents("programming language", n_results=2)
        self.assertEqual(len(results), 2)
        
        # Check that most relevant document is about Python
        self.assertIn("python", results[0]['document'].lower())

if __name__ == "__main__":
    unittest.main()
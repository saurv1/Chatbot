"""
Tests for the chatbot functionality
"""
import unittest
from app.core.chatbot import TutorChatbot
from app.core.memory import ChatMemory

class TestChatbot(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.chatbot = TutorChatbot(model_name="distilgpt2", use_rag=False)
    
    def test_chatbot_initialization(self):
        """Test chatbot initialization"""
        self.assertIsNotNone(self.chatbot.llm)
        self.assertIsNotNone(self.chatbot.memory)
    
    def test_memory_functionality(self):
        """Test conversation memory"""
        # Test adding messages
        self.chatbot.memory.add_message("Hello", is_user=True)
        self.chatbot.memory.add_message("Hi there!", is_user=False)
        
        messages = self.chatbot.memory.get_messages()
        self.assertEqual(len(messages), 2)
        
        # Test clearing memory
        self.chatbot.clear_conversation()
        messages = self.chatbot.memory.get_messages()
        self.assertEqual(len(messages), 0)
    
    def test_response_generation(self):
        """Test basic response generation"""
        response = self.chatbot.generate_response("Hello, how are you?")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

if __name__ == "__main__":
    unittest.main()
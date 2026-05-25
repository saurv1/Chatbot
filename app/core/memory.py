"""
Memory management
"""
from typing import List

class SimpleMessage:
    def __init__(self, content: str, is_user: bool = True):
        self.content = content
        self.is_user = is_user

class ChatMemory:
    def __init__(self, memory_type: str = "buffer", window_size: int = 6):
        """
        Initialize chat memory - FIXED
        """
        self.memory_type = memory_type
        self.window_size = window_size  # Number of exchanges to keep
        self.messages = []
    
    def add_message(self, message: str, is_user: bool = True):
        """Add a message to memory"""
        self.messages.append(SimpleMessage(message, is_user))
        
        # If using window memory, trim old messages
        if self.memory_type == "window" and len(self.messages) > self.window_size * 2:
            # Keep only the most recent messages
            self.messages = self.messages[-(self.window_size * 2):]
    
    def get_messages(self) -> List[SimpleMessage]:
        """Get all messages from memory"""
        return self.messages
    
    def get_conversation_history(self) -> str:
        """Get conversation history as formatted string"""
        history = []
        for msg in self.messages:
            role = "Student" if msg.is_user else "Tutor"
            history.append(f"{role}: {msg.content}")
        return "\n".join(history)
    
    def clear_memory(self):
        """Clear all memory"""
        self.messages = []
"""
FastAPI endpoints for the chatbot tutor - FIXED VERSION
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Create router
router = APIRouter()

# Define models FIRST to avoid NameError
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

class DocumentAddRequest(BaseModel):
    documents: List[str]
    metadatas: Optional[List[dict]] = None

class DocumentAddResponse(BaseModel):
    success: bool
    message: str
    documents_added: int

class MemoryClearRequest(BaseModel):
    session_id: str

class MemoryClearResponse(BaseModel):
    success: bool
    message: str

class ModelConfig(BaseModel):
    model_name: Optional[str] = None
    use_rag: bool = True

# Import with model selection
try:
    from ..core.chatbot import TutorChatbot
    from ..core.rag import RAGSystem
    from ..core.model_selector import get_recommended_model
    
    # Use recommended model by default
    DEFAULT_MODEL = get_recommended_model()
    print(f"🎯 API using model: {DEFAULT_MODEL}")
    
    # Initialize components
    chatbot = TutorChatbot(model_name=DEFAULT_MODEL)
    rag_system = RAGSystem()
    CHATBOT_AVAILABLE = True
    
except Exception as e:
    print(f"❌ Chatbot initialization failed: {e}")
    CHATBOT_AVAILABLE = False
    chatbot = None
    rag_system = None
    DEFAULT_MODEL = "distilgpt2"

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Send a message to the chatbot and get response"""
    if not CHATBOT_AVAILABLE or chatbot is None:
        return ChatResponse(
            response="Chatbot service is currently unavailable. Please try again later.",
            session_id=request.session_id
        )
    
    try:
        print(f"📨 Received message: {request.message}")
        response = chatbot.generate_response(request.message)
        print(f"📤 Sending response: {response[:100]}...")
        return ChatResponse(response=response, session_id=request.session_id)
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return ChatResponse(
            response="I encountered an error while processing your question. Please try again.",
            session_id=request.session_id
        )

@router.post("/chat_with_config", response_model=ChatResponse)
async def chat_with_config_endpoint(request: ChatRequest, config: ModelConfig):
    """Chat endpoint with model configuration"""
    if not CHATBOT_AVAILABLE:
        raise HTTPException(status_code=503, detail="Chatbot service unavailable")
    
    try:
        # Use specified model or default
        model_to_use = config.model_name or DEFAULT_MODEL
        
        # Create new chatbot instance with specified configuration
        current_chatbot = TutorChatbot(model_name=model_to_use, use_rag=config.use_rag)
            
        response = current_chatbot.generate_response(request.message)
        return ChatResponse(response=response, session_id=request.session_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.post("/documents/add", response_model=DocumentAddResponse)
async def add_documents(request: DocumentAddRequest):
    """Add documents to the RAG system"""
    if not CHATBOT_AVAILABLE or rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system unavailable")
    
    try:
        rag_system.add_documents(request.documents, request.metadatas)
        return DocumentAddResponse(
            success=True,
            message="Documents added successfully",
            documents_added=len(request.documents)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding documents: {str(e)}")

@router.post("/memory/clear", response_model=MemoryClearResponse)
async def clear_memory(request: MemoryClearRequest):
    """Clear conversation memory for a session"""
    if not CHATBOT_AVAILABLE or chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot service unavailable")
    
    try:
        chatbot.clear_conversation()
        return MemoryClearResponse(
            success=True,
            message="Memory cleared successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    status = "healthy" if CHATBOT_AVAILABLE else "degraded"
    return {
        "status": status, 
        "service": "chatbot-tutor-api", 
        "chatbot_available": CHATBOT_AVAILABLE,
        "current_model": DEFAULT_MODEL if CHATBOT_AVAILABLE else "unknown"
    }

@router.get("/models/available")
async def get_available_models():
    """Get list of available models"""
    available_models = [
        "microsoft/DialoGPT-medium",
        "microsoft/DialoGPT-small", 
        "gpt2",
        "distilgpt2"
    ]
    return {"available_models": available_models}

@router.get("/models/current")
async def get_current_model():
    """Get current model info"""
    if chatbot and CHATBOT_AVAILABLE:
        return {
            "current_model": chatbot.model_name,
            "is_instruction_tuned": getattr(chatbot, 'is_instruction_tuned', False),
            "rag_enabled": chatbot.use_rag
        }
    return {"error": "Chatbot not available"}

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Chatbot Tutor API is running", 
        "version": "1.0.0",
        "model": DEFAULT_MODEL
    }
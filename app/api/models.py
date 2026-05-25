"""
Pydantic models for API requests/responses
"""
from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

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
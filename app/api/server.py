"""
FastAPI server configuration - Fixed for compatibility
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import router as api_router  # Changed from 'app' to 'router'

def create_app():
    """Create and configure FastAPI application"""
    app = FastAPI(title="Chatbot Tutor API", version="1.0.0")
    
    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    from .endpoints import router as api_router
    app.include_router(api_router, prefix="/api/v1")
    
    return app  # Make sure this line exists!

# Remove the run_server function or keep it simple
def run_server():
    """Run the server"""
    app = create_app()
    return app
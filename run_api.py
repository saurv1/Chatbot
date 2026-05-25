"""
FastAPI server runner - Fixed version
"""
import uvicorn
import sys
import os

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Use import string format to avoid reload warning
    uvicorn.run(
        "app.api.server:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True  # Use factory function
    )
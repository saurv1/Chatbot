"""
Web interface utilities (simplified)
"""
def run_web():
    """Run Streamlit web interface"""
    import subprocess
    import sys
    import os
    
    # Add app directory to Python path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "app/frontend/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
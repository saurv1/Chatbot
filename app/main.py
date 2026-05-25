"""
Main application entry point for Chatbot Tutor (simplified)
"""
import argparse
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.chatbot import TutorChatbot
from core.rag import RAGSystem

def main():
    """Main application function"""
    parser = argparse.ArgumentParser(description="Chatbot Tutor with Memory")
    parser.add_argument("--mode", choices=["cli", "api", "web", "flask"], default="cli", 
                       help="Run mode: cli, api, web, or flask")
    parser.add_argument("--model", default="gpt2", help="Hugging Face model name")
    parser.add_argument("--port", type=int, default=8000, help="API port")
    parser.add_argument("--load-samples", action="store_true", help="Load sample documents")
    parser.add_argument("--no-rag", action="store_true", help="Disable RAG")
    
    args = parser.parse_args()
    
    # Initialize components
    print("Initializing Chatbot Tutor...")
    chatbot = TutorChatbot(model_name=args.model, use_rag=not args.no_rag)
    
    if args.load_samples and chatbot.rag_system:
        rag_system = RAGSystem()
        rag_system.load_sample_documents("./data/sample_documents")
        print("✅ Sample documents loaded!")
    
    print(f"✅ Chatbot initialized with model: {args.model}")
    print(f"✅ RAG enabled: {not args.no_rag}")
    
    if args.mode == "cli":
        from interfaces.cli import run_cli
        run_cli(chatbot)
    elif args.mode == "api":
        from api.server import run_server
        print(f"🚀 Starting API server on port {args.port}...")
        run_server(port=args.port)
    elif args.mode == "web":
        from interfaces.web import run_web
        print("🌐 Starting Streamlit web interface...")
        run_web()
    elif args.mode == "flask":
        from frontend.flask_app import run_flask
        print(f"🌐 Starting Flask web interface on port {args.port}...")
        run_flask(port=args.port)

if __name__ == "__main__":
    main()
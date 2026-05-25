"""
Command Line Interface for the Chatbot Tutor
"""
import argparse
from app.core.chatbot import TutorChatbot
from app.core.rag import RAGSystem

def main():
    parser = argparse.ArgumentParser(description="Chatbot Tutor CLI")
    parser.add_argument("--model", default="gpt2", help="Hugging Face model name")
    parser.add_argument("--no-rag", action="store_true", help="Disable RAG")
    parser.add_argument("--load-samples", action="store_true", help="Load sample documents")
    
    args = parser.parse_args()
    
    # Initialize chatbot
    chatbot = TutorChatbot(model_name=args.model, use_rag=not args.no_rag)
    
    # Load sample documents if requested
    if args.load_samples and chatbot.rag_system:
        rag_system = RAGSystem()
        rag_system.load_sample_documents("./data/sample_documents")
        print("Sample documents loaded!")
    
    print("🤖 Chatbot Tutor CLI")
    print("Type 'quit' to exit, 'clear' to clear memory")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'clear':
                chatbot.clear_conversation()
                print("Memory cleared!")
                continue
            
            # Generate response
            response = chatbot.generate_response(user_input)
            print(f"Tutor: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
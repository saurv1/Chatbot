"""
CLI interface for Chatbot Tutor
"""
def run_cli(chatbot):
    """Run command line interface"""
    print("🤖 Chatbot Tutor CLI")
    print("Type 'quit' to exit, 'clear' to clear memory")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            elif user_input.lower() in ['clear', 'reset']:
                chatbot.clear_conversation()
                print("Memory cleared!")
                continue
            elif user_input.lower() in ['help', '?']:
                print("\nAvailable commands:")
                print("  help, ?     - Show this help")
                print("  clear, reset - Clear conversation memory")
                print("  quit, exit, q - Exit the program")
                continue
            
            # Generate response
            print("Tutor: ", end="", flush=True)
            response = chatbot.generate_response(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\nError: {e}")
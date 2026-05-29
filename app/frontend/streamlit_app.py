"""
Streamlit web interface with improved connection handling
"""
import streamlit as st
import requests
import time

# API configuration - try different ports if needed
API_BASE_URL = "http://localhost:8000"
API_PATHS = [
    "/api/v1/health",
    "/health",
    "/"
]

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = "default_session"
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your educational assistant. How can I help you learn today?"}
        ]
    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = False
    if 'api_base_url' not in st.session_state:
        st.session_state.api_base_url = API_BASE_URL

def find_api_endpoint():
    """Try to find the correct API endpoint"""
    for path in API_PATHS:
        try:
            url = f"{API_BASE_URL}{path}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                st.session_state.api_base_url = API_BASE_URL
                return True
        except:
            continue
    
    # Try alternative ports
    for port in [8000, 8001, 8080]:
        try:
            url = f"http://localhost:{port}/health"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                st.session_state.api_base_url = f"http://localhost:{port}"
                return True
        except:
            continue
    
    return False

def check_api_connection():
    """Check if API is available"""
    try:
        if find_api_endpoint():
            st.session_state.api_connected = True
            return True
    except Exception as e:
        st.error(f"Connection error: {e}")
    
    st.session_state.api_connected = False
    return False

def send_message_to_api(message: str) -> str:
    """Send message to API and get response"""
    try:
        payload = {
            "message": message,
            "session_id": st.session_state.session_id
        }
        
        # Try different endpoint paths
        endpoints = ["/api/v1/chat", "/chat"]
        
        for endpoint in endpoints:
            try:
                url = f"{st.session_state.api_base_url}{endpoint}"
                response = requests.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json()["response"]
            except:
                continue
        
        return "Sorry, I couldn't connect to the AI service. Please make sure the API server is running."
        
    except Exception as e:
        return f"Error: {str(e)}"

def clear_conversation():
    """Clear conversation memory"""
    st.session_state.messages = [
        {"role": "assistant", "content": "Conversation cleared! How can I help you learn today?"}
    ]

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Chatbot Tutor",
        page_icon="🎓",
        layout="wide"
    )
    
    initialize_session_state()
    
    # Header
    st.title("🎓 Chatbot Tutor with Memory")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # API status with auto-refresh
        if check_api_connection():
            st.success(" API Connected")
            st.info(f"Connected to: {st.session_state.api_base_url}")
        else:
            st.error(" API Not Connected")
            st.info("Please make sure the API server is running on port 8000")
            
            if st.button(" Retry Connection"):
                st.rerun()
        
        # Session management
        st.session_state.session_id = st.text_input(
            "Session ID",
            value=st.session_state.session_id
        )
        
        if st.button(" Clear Conversation", use_container_width=True):
            clear_conversation()
            st.rerun()
        
        st.markdown("---")
        st.info("""
        **Troubleshooting:**
        - Ensure API server is running
        - Check if port 8000 is available
        - Try refreshing the page
        """)
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask your tutor a question..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get and display assistant response
            with st.chat_message("assistant"):
                if st.session_state.api_connected:
                    with st.spinner("Thinking..."):
                        response = send_message_to_api(prompt)
                    st.markdown(response)
                else:
                    st.error("API not connected. Please start the API server first.")
                    response = "I'm unable to connect to the AI service. Please check if the API server is running."
            
            # Add assistant response to chat history
            if st.session_state.api_connected:
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    with col2:
        st.header("Learning Resources")
        st.info("""
        **Sample questions:**
        - What is mathematics?
        - Explain physics basics
        - Programming concepts
        - Calculus introduction
        """)
        
        if st.button("📚 Test Connection", use_container_width=True):
            test_response = send_message_to_api("Hello")
            st.info(f"Test response: {test_response[:100]}...")

if __name__ == "__main__":
    main()
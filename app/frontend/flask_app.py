"""
Flask web interface as an alternative to Streamlit
"""
from flask import Flask, render_template, request, jsonify
import requests
import os

# API configuration
API_BASE_URL = "http://localhost:8000"

def create_flask_app():
    """Create Flask application"""
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/chat', methods=['POST'])
    def api_chat():
        """Chat endpoint that proxies to FastAPI"""
        try:
            data = request.json
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            return jsonify(response.json()), response.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/health')
    def api_health():
        """Health check endpoint"""
        try:
            response = requests.get(f"{API_BASE_URL}/health")
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({"status": "API not available"}), 503
    
    @app.route('/api/clear', methods=['POST'])
    def api_clear():
        """Clear memory endpoint"""
        try:
            data = request.json
            response = requests.post(
                f"{API_BASE_URL}/memory/clear",
                json=data
            )
            return jsonify(response.json()), response.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app

def run_flask(host="0.0.0.0", port=5000, debug=True):
    """Run Flask web interface"""
    app = create_flask_app()
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    run_flask()
from http.server import BaseHTTPRequestHandler
import json
import os
import asyncio
from typing import Dict, Any
import sys
import traceback

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from open_deep_research.deep_researcher import deep_researcher
    from open_deep_research.configuration import Configuration
    from langchain_core.messages import HumanMessage
except ImportError as e:
    print(f"Import error: {e}")
    traceback.print_exc()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Handle CORS
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()

            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract message from request
            messages = data.get('input', {}).get('messages', [])
            if not messages:
                self.wfile.write(b'{"error": "No messages provided"}')
                return

            # Get the latest user message
            user_message = messages[-1]['content']

            # Initialize configuration
            config = {
                "configurable": {
                    "model_name": "gpt-4o",
                    "search_api": "tavily"
                }
            }

            # Create the researcher graph
            app = deep_researcher

            # Run the research
            response_text = ""
            for chunk in app.stream(
                {"messages": [HumanMessage(content=user_message)]},
                config=config
            ):
                if 'final_response' in chunk:
                    response_text = chunk['final_response']['messages'][-1].content
                    
            # Send response
            self.wfile.write(f"data: {json.dumps({'content': response_text})}\n\n".encode())
            
        except Exception as e:
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.wfile.write(f"data: {json.dumps({'error': error_msg})}\n\n".encode())

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers() 
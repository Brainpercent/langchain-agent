from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import traceback

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    from open_deep_research.deep_researcher import deep_researcher
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
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()

            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract message from request
            messages = data.get('input', {}).get('messages', [])
            if not messages:
                self.wfile.write(b'data: {"error": "No messages provided"}\n\n')
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

            # Send initial response
            self.wfile.write(b'data: {"type": "start"}\n\n')
            self.wfile.flush()

            # Create the researcher graph
            app = deep_researcher

            # Stream the research process
            full_response = ""
            for chunk in app.stream(
                {"messages": [HumanMessage(content=user_message)]},
                config=config
            ):
                if 'messages' in chunk:
                    # Extract content from the chunk
                    for message in chunk['messages']:
                        if hasattr(message, 'content'):
                            content = message.content
                            full_response += content
                            # Send chunk
                            chunk_data = json.dumps({
                                "type": "chunk",
                                "content": content
                            })
                            self.wfile.write(f"data: {chunk_data}\n\n".encode())
                            self.wfile.flush()

            # Send final response
            final_data = json.dumps({
                "type": "complete",
                "content": full_response
            })
            self.wfile.write(f"data: {final_data}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            error_data = json.dumps({"error": error_msg})
            self.wfile.write(f"data: {error_data}\n\n".encode())

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers() 
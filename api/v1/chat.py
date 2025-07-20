from http.server import BaseHTTPRequestHandler
import json
import os
import time
import hashlib
import hmac
from urllib.parse import parse_qs
import asyncio
import aiohttp

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-API-Key')
            self.end_headers()

            # Get request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_error_response("Invalid JSON format", 400)
                return

            # Authenticate request
            api_key = self.headers.get('X-API-Key') or self.headers.get('Authorization', '').replace('Bearer ', '')
            if not self.validate_api_key(api_key):
                self.send_error_response("Invalid or missing API key", 401)
                return

            # Rate limiting check
            if not self.check_rate_limit(api_key):
                self.send_error_response("Rate limit exceeded", 429)
                return

            # Process the chat request
            response = self.process_chat_request(data)
            
            # Log usage
            self.log_usage(api_key, data.get('platform', 'unknown'))
            
            # Send response
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"Error in chat API: {str(e)}")
            self.send_error_response("Internal server error", 500)

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-API-Key')
        self.end_headers()

    def validate_api_key(self, api_key):
        """Validate API key - in production, check against database"""
        if not api_key:
            return False
        
        # For demo, accept specific test keys
        valid_keys = [
            'demo-whatsapp-key-12345',
            'demo-telegram-key-67890',
            'demo-webhook-key-abcde'
        ]
        
        # In production, validate against Supabase database
        return api_key in valid_keys or api_key.startswith('ak_')

    def check_rate_limit(self, api_key):
        """Check rate limiting - in production, use Redis"""
        # For demo, always allow
        # In production: implement per-key rate limiting
        return True

    def process_chat_request(self, data):
        """Process the chat request and call LangGraph API"""
        start_time = time.time()
        
        # Extract request data
        message = data.get('message', '')
        platform = data.get('platform', 'webhook')
        user_id = data.get('user_id', 'anonymous')
        channel_id = data.get('channel_id', '')
        
        if not message:
            raise ValueError("Message is required")

        try:
            # Call LangGraph API
            research_response = self.call_langgraph_api(message)
            
            # Format response based on platform
            formatted_response = self.format_response_for_platform(
                research_response, platform
            )
            
            processing_time = time.time() - start_time
            
            return {
                "status": "success",
                "response": formatted_response,
                "platform": platform,
                "user_id": user_id,
                "channel_id": channel_id,
                "processing_time": round(processing_time, 2),
                "timestamp": int(time.time()),
                "tokens_estimated": len(formatted_response.split()) * 1.3
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "platform": platform,
                "user_id": user_id,
                "processing_time": time.time() - start_time
            }

    def call_langgraph_api(self, message):
        """Call the LangGraph API for research"""
        # This would be async in production, simplified for serverless
        
        # Mock response for demo - replace with actual LangGraph call
        langgraph_url = os.environ.get('LANGGRAPH_API_URL', 'http://localhost:2024')
        assistant_id = os.environ.get('ASSISTANT_ID', 'research-assistant')
        
        # For demo, return formatted research response
        return f"""# Research Results for: "{message}"

Based on my analysis, here are the key findings:

## Summary
This is a comprehensive research response that would normally come from the LangGraph API. The system has analyzed multiple sources and synthesized the information.

## Key Points
• **Point 1**: Detailed information about the research topic
• **Point 2**: Additional insights and analysis
• **Point 3**: Relevant trends and patterns

## Sources
- [Academic Source](https://example.com/source1)
- [Industry Report](https://example.com/source2)
- [Recent News](https://example.com/source3)

## Conclusion
The research indicates significant developments in this area, with implications for future trends and applications.

*Research completed in {time.strftime('%Y-%m-%d %H:%M:%S')}*"""

    def format_response_for_platform(self, response, platform):
        """Format response based on target platform"""
        
        if platform == 'whatsapp':
            # WhatsApp formatting (no markdown, simple formatting)
            formatted = response.replace('# ', '*').replace('## ', '*').replace('**', '*')
            formatted = formatted.replace('• ', '• ')  # Keep bullet points
            # Remove markdown links and keep just the text
            import re
            formatted = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', formatted)
            return formatted
            
        elif platform == 'telegram':
            # Telegram supports markdown
            formatted = response.replace('# ', '*').replace('## ', '*')
            return formatted
            
        elif platform == 'discord':
            # Discord markdown support
            return response
            
        else:
            # Default webhook format (full markdown)
            return response

    def log_usage(self, api_key, platform):
        """Log API usage for analytics"""
        # In production, log to database
        print(f"API Usage: {api_key[:10]}... on {platform} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    def send_error_response(self, message, status_code):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_response = {
            "status": "error",
            "error": message,
            "timestamp": int(time.time())
        }
        
        self.wfile.write(json.dumps(error_response).encode('utf-8')) 
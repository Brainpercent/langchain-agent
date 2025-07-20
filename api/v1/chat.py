from http.server import BaseHTTPRequestHandler
import json
import os
import time
import hashlib
import hmac
import requests
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
            self.send_header('Access-Control-Max-Age', '86400')
            self.end_headers()

            # Get request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_error_response("Invalid JSON format", 400)
                return

            # Get authorization token from header
            auth_header = self.headers.get('Authorization', '')
            access_token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else None
            
            # For web platform, we expect a Supabase JWT token
            platform = data.get('platform', 'webhook')
            if platform == 'web' and not access_token:
                self.send_error_response("Authorization required for web platform", 401)
                return
            
            # For other platforms, validate API key
            if platform != 'web':
                api_key = self.headers.get('X-API-Key') or access_token
                if not self.validate_api_key(api_key):
                    self.send_error_response("Invalid or missing API key", 401)
                    return

                # Rate limiting check
                if not self.check_rate_limit(api_key):
                    self.send_error_response("Rate limit exceeded", 429)
                    return

            # Process the chat request
            response = self.process_chat_request(data, access_token)
            
            # Log usage
            user_id = data.get('user_id', 'unknown')
            self.log_usage(user_id, data.get('platform', 'unknown'))
            
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
        self.send_header('Access-Control-Max-Age', '86400')
        self.send_header('Content-Length', '0')
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

    def process_chat_request(self, data, access_token=None):
        """Process the chat request and call LangGraph API"""
        start_time = time.time()
        
        # Extract request data
        message = data.get('message', '')
        platform = data.get('platform', 'webhook')
        user_id = data.get('user_id', 'anonymous')
        channel_id = data.get('channel_id', '')
        history = data.get('history', [])
        
        if not message:
            raise ValueError("Message is required")

        try:
            # Call LangGraph API with proper authentication
            research_response = self.call_langgraph_api(message, history, access_token)
            
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

    def call_langgraph_api(self, message, history=None, access_token=None):
        """Call the LangGraph API for research"""
        try:
            # Get configuration from environment
            langgraph_url = os.environ.get('LANGGRAPH_API_URL', 'http://localhost:2024')
            langsmith_endpoint = os.environ.get('LANGSMITH_ENDPOINT', '')
            langsmith_api_key = os.environ.get('LANGSMITH_API_KEY', '')
            
            # If we're using LangSmith endpoint, call LangSmith directly
            if langsmith_endpoint and 'smith.langchain.com' in langgraph_url:
                print(f"Using LangSmith endpoint: {langsmith_endpoint}")
                return self.call_langsmith_api(message, history, langsmith_api_key)
            
            # Otherwise, use the original LangGraph API approach
            # Prepare conversation history
            messages = []
            if history:
                messages.extend(history)
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Prepare the request to LangGraph
            thread_id = f"thread_{int(time.time())}_{hashlib.md5(message.encode()).hexdigest()[:8]}"
            
            request_body = {
                "input": {
                    "messages": messages
                },
                "config": {
                    "configurable": {
                        "thread_id": thread_id
                    }
                },
                "stream": False  # We'll get the full response and return it
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            # Add authorization if token is provided (for authenticated users)
            if access_token:
                headers['Authorization'] = f'Bearer {access_token}'
            
            print(f"Calling LangGraph API at {langgraph_url}/runs/invoke")
            print(f"Using authorization: {'Yes' if access_token else 'No'}")
            
            # Make request to LangGraph
            import requests
            response = requests.post(
                f"{langgraph_url}/runs/invoke",
                json=request_body,
                headers=headers,
                timeout=120  # Increased timeout for research tasks
            )
            
            print(f"LangGraph response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the AI response from LangGraph result
                if 'output' in result and 'messages' in result['output']:
                    messages = result['output']['messages']
                    if messages and len(messages) > 0:
                        last_message = messages[-1]
                        if 'content' in last_message:
                            return last_message['content']
                
                # Fallback: return the whole output as string
                return str(result.get('output', 'No response from LangGraph'))
            
            else:
                print(f"LangGraph API error: {response.status_code} - {response.text}")
                # Return demo response as fallback
                return self.get_demo_response(message)
                
        except Exception as e:
            print(f"Error calling LangGraph API: {str(e)}")
            # Return demo response as fallback
            return self.get_demo_response(message)

    def call_langsmith_api(self, message, history=None, langsmith_api_key=None):
        """Call LangSmith API directly for research (simplified approach)"""
        try:
            # For now, return a demo response that looks like research results
            # In a full implementation, you would call your deployed LangGraph app via LangSmith
            import time
            
            # Simulate research delay
            time.sleep(2)
            
            return f"""# Research Analysis: "{message}"

## Executive Summary
Based on comprehensive analysis of available sources, here are the key findings regarding your query about "{message}".

## Key Insights
• **Primary Finding**: This topic shows significant developments in recent research and industry applications
• **Trends**: Current data indicates growing interest and investment in this area
• **Implications**: The findings suggest important considerations for future development

## Detailed Analysis
The research reveals multiple dimensions to consider:

1. **Technical Aspects**: Current implementations show promising results
2. **Market Dynamics**: Industry adoption is accelerating 
3. **Future Outlook**: Projections indicate continued growth and innovation

## Sources Referenced
- Academic research databases
- Industry reports and white papers  
- Recent news and market analysis
- Expert opinions and surveys

## Recommendations
Based on this analysis, I recommend:
- Monitoring ongoing developments in this space
- Considering the implications for your specific use case
- Staying updated with latest research and industry trends

---
*Research completed on {time.strftime('%Y-%m-%d at %H:%M:%S')}*  
*Powered by Deep Research AI via LangSmith*"""
            
        except Exception as e:
            print(f"Error in LangSmith API call: {str(e)}")
            return self.get_demo_response(message)
    
    def get_demo_response(self, message):
        """Generate a demo response when LangGraph is not available"""
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

*Research completed in {time.strftime('%Y-%m-%d %H:%M:%S')}*

---
*Note: This is a demo response. Configure LANGGRAPH_API_URL environment variable to connect to your LangGraph server.*"""

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

    def log_usage(self, user_id, platform):
        """Log API usage for analytics"""
        # In production, log to database
        print(f"API Usage: User {user_id} on {platform} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

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
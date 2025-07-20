import json
import os
import time
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-API-Key')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

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
                error_response = {"status": "error", "error": "Invalid JSON format"}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return

            # Extract request data
            message = data.get('message', '')
            platform = data.get('platform', 'web')
            user_id = data.get('user_id', 'anonymous')
            history = data.get('history', [])
            
            if not message:
                error_response = {"status": "error", "error": "Message is required"}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return

            # Get authorization token
            auth_header = self.headers.get('Authorization', '')
            access_token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else None

            # Call your actual LangGraph research assistant
            try:
                research_response = self.call_langgraph_research(message, history, access_token)
            except Exception as e:
                print(f"Error calling LangGraph: {str(e)}")
                research_response = self.get_demo_response(message)
            
            response_data = {
                "status": "success",
                "response": research_response,
                "platform": platform,
                "user_id": user_id,
                "processing_time": 2.5,
                "timestamp": int(time.time())
            }
            
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        except Exception as e:
            print(f"Error in chat API: {str(e)}")
            error_response = {
                "status": "error",
                "error": f"Internal server error: {str(e)}",
                "timestamp": int(time.time())
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def call_langgraph_research(self, message, history=None, access_token=None):
        """Call your actual LangGraph research assistant"""
        
        # If you have LangGraph deployed to LangGraph Cloud, use that URL
        # Otherwise, this will use the demo response
        langgraph_url = os.environ.get('LANGGRAPH_API_URL', '')
        
        if langgraph_url and 'localhost' not in langgraph_url:
            # Prepare conversation history
            messages = []
            if history:
                messages.extend(history)
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Prepare the request to LangGraph
            thread_id = f"thread_{int(time.time())}"
            
            request_body = {
                "input": {
                    "messages": messages
                },
                "config": {
                    "configurable": {
                        "thread_id": thread_id
                    }
                },
                "stream": False
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            # Add authorization if token is provided
            if access_token:
                headers['Authorization'] = f'Bearer {access_token}'
            
            try:
                response = requests.post(
                    f"{langgraph_url}/runs/invoke",
                    json=request_body,
                    headers=headers,
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract the AI response from LangGraph result
                    if 'output' in result and 'messages' in result['output']:
                        messages = result['output']['messages']
                        if messages and len(messages) > 0:
                            last_message = messages[-1]
                            if 'content' in last_message:
                                return last_message['content']
                    
                    return str(result.get('output', 'No response from LangGraph'))
                
            except Exception as e:
                print(f"Error calling LangGraph API: {str(e)}")
        
        # Fallback to demo response
        return self.get_demo_response(message)

    def get_demo_response(self, message):
        """Generate a demo response when LangGraph is not available"""
        return f"""# Research Analysis: "{message}"

## Executive Summary
Based on comprehensive analysis, here are the key findings regarding "{message}".

## Key Insights
• **Primary Finding**: This topic shows significant developments in recent research
• **Trends**: Current data indicates growing interest and investment
• **Implications**: Important considerations for future development

## Detailed Analysis
The research reveals multiple dimensions:
1. **Technical Aspects**: Current implementations show promising results
2. **Market Dynamics**: Industry adoption is accelerating
3. **Future Outlook**: Projections indicate continued growth

## Recommendations
- Monitor ongoing developments in this space
- Consider implications for your specific use case
- Stay updated with latest research trends

---
*Research completed on {time.strftime('%Y-%m-%d at %H:%M:%S')}*
*Powered by Deep Research AI (Demo Mode)*

**Note**: To use your actual LangGraph research assistant, deploy it to LangGraph Cloud and set the LANGGRAPH_API_URL environment variable in Vercel.""" 
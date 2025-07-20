from http.server import BaseHTTPRequestHandler
import json
import os
import hmac
import hashlib
import time
import requests
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle WhatsApp webhook verification"""
        try:
            # Parse query parameters
            query_components = dict(qc.split("=") for qc in self.path.split("?")[1].split("&"))
            
            mode = query_components.get('hub.mode', '')
            token = query_components.get('hub.verify_token', '')
            challenge = query_components.get('hub.challenge', '')
            
            # Verify token
            verify_token = os.environ.get('WHATSAPP_VERIFY_TOKEN', 'your_verify_token_here')
            
            if mode == 'subscribe' and token == verify_token:
                print("WhatsApp webhook verified successfully")
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(challenge.encode('utf-8'))
            else:
                print("WhatsApp webhook verification failed")
                self.send_response(403)
                self.end_headers()
                
        except Exception as e:
            print(f"WhatsApp verification error: {str(e)}")
            self.send_response(400)
            self.end_headers()

    def do_POST(self):
        """Handle incoming WhatsApp messages"""
        try:
            # CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Get request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Verify webhook signature (security)
            if not self.verify_webhook_signature(post_data):
                print("WhatsApp webhook signature verification failed")
                return

            try:
                webhook_data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                print("Invalid JSON in WhatsApp webhook")
                return

            # Process WhatsApp webhook
            self.process_whatsapp_webhook(webhook_data)
            
            # Send 200 OK response
            response = {"status": "success"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"Error processing WhatsApp webhook: {str(e)}")
            self.send_response(500)
            self.end_headers()

    def verify_webhook_signature(self, payload):
        """Verify WhatsApp webhook signature"""
        signature_header = self.headers.get('X-Hub-Signature-256', '')
        if not signature_header:
            return False
            
        app_secret = os.environ.get('WHATSAPP_APP_SECRET', '')
        if not app_secret:
            print("WhatsApp app secret not configured")
            return True  # Skip verification in development
            
        expected_signature = hmac.new(
            app_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return signature_header == f'sha256={expected_signature}'

    def process_whatsapp_webhook(self, webhook_data):
        """Process incoming WhatsApp message"""
        try:
            # Extract message data
            entry = webhook_data.get('entry', [])
            if not entry:
                return

            for entry_item in entry:
                changes = entry_item.get('changes', [])
                for change in changes:
                    value = change.get('value', {})
                    messages = value.get('messages', [])
                    
                    for message in messages:
                        self.handle_whatsapp_message(message, value)

        except Exception as e:
            print(f"Error processing WhatsApp message: {str(e)}")

    def handle_whatsapp_message(self, message, value):
        """Handle individual WhatsApp message"""
        try:
            message_type = message.get('type', '')
            from_number = message.get('from', '')
            message_id = message.get('id', '')
            timestamp = message.get('timestamp', '')
            
            # Only process text messages
            if message_type != 'text':
                return
                
            text_content = message.get('text', {}).get('body', '')
            if not text_content:
                return

            print(f"WhatsApp message from {from_number}: {text_content}")

            # Call our chat API to get research response
            research_response = self.get_research_response(text_content, from_number)
            
            # Send response back via WhatsApp
            if research_response:
                self.send_whatsapp_message(from_number, research_response)

        except Exception as e:
            print(f"Error handling WhatsApp message: {str(e)}")

    def get_research_response(self, message, user_id):
        """Get research response from our chat API"""
        try:
            chat_api_url = os.environ.get('CHAT_API_URL', 'https://your-vercel-app.vercel.app/api/v1/chat')
            
            payload = {
                "message": message,
                "platform": "whatsapp",
                "user_id": user_id,
                "channel_id": "whatsapp_direct"
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': 'demo-whatsapp-key-12345'  # Use your API key
            }
            
            response = requests.post(chat_api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    return result.get('response', '')
            
            return "I'm having trouble processing your request right now. Please try again later."
            
        except Exception as e:
            print(f"Error getting research response: {str(e)}")
            return "I'm experiencing technical difficulties. Please try again."

    def send_whatsapp_message(self, to_number, message):
        """Send message via WhatsApp Business API"""
        try:
            access_token = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')
            phone_number_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')
            
            if not access_token or not phone_number_id:
                print("WhatsApp credentials not configured")
                return False

            url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Split long messages for WhatsApp
            max_length = 4096
            if len(message) > max_length:
                # Split message into chunks
                chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
                for i, chunk in enumerate(chunks):
                    if i > 0:
                        chunk = f"({i+1}/{len(chunks)}) {chunk}"
                    self.send_single_whatsapp_message(url, headers, to_number, chunk)
            else:
                self.send_single_whatsapp_message(url, headers, to_number, message)
                
            return True
            
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False

    def send_single_whatsapp_message(self, url, headers, to_number, message):
        """Send a single WhatsApp message"""
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "text": {"body": message}
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"WhatsApp message sent successfully to {to_number}")
        else:
            print(f"Failed to send WhatsApp message: {response.status_code} - {response.text}")

    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers() 
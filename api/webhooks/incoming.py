from http.server import BaseHTTPRequestHandler
import json
import os
import time
import hmac
import hashlib
import requests
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle incoming webhook from external systems"""
        try:
            # CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-API-Key, X-Webhook-Signature')
            self.end_headers()

            # Get request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Authenticate request
            api_key = self.headers.get('X-API-Key') or self.headers.get('Authorization', '').replace('Bearer ', '')
            if not self.validate_api_key(api_key):
                self.send_error_response("Invalid or missing API key", 401)
                return

            # Verify webhook signature if provided
            if not self.verify_webhook_signature(post_data, api_key):
                self.send_error_response("Invalid webhook signature", 401)
                return

            try:
                webhook_data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_error_response("Invalid JSON format", 400)
                return

            # Process the webhook
            response = self.process_incoming_webhook(webhook_data, api_key)
            
            # Log usage
            self.log_webhook_usage(api_key, webhook_data.get('type', 'unknown'))
            
            # Send response
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"Error in incoming webhook: {str(e)}")
            self.send_error_response("Internal server error", 500)

    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-API-Key, X-Webhook-Signature')
        self.end_headers()

    def validate_api_key(self, api_key):
        """Validate API key"""
        if not api_key:
            return False
        
        # For demo, accept test keys
        valid_keys = [
            'demo-webhook-key-abcde',
            'demo-integration-key-12345'
        ]
        
        return api_key in valid_keys or api_key.startswith('ak_')

    def verify_webhook_signature(self, payload, api_key):
        """Verify webhook signature if provided"""
        signature_header = self.headers.get('X-Webhook-Signature', '')
        if not signature_header:
            return True  # No signature required for demo
            
        # In production, get the webhook secret for this API key from database
        webhook_secret = os.environ.get('WEBHOOK_SECRET', api_key + '_secret')
        
        if signature_header.startswith('sha256='):
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            return signature_header == f'sha256={expected_signature}'
        
        return False

    def process_incoming_webhook(self, webhook_data, api_key):
        """Process the incoming webhook data"""
        start_time = time.time()
        
        try:
            # Extract webhook type and data
            webhook_type = webhook_data.get('type', 'message')
            message = webhook_data.get('message', '')
            user_id = webhook_data.get('user_id', 'webhook_user')
            source_system = webhook_data.get('source_system', 'external')
            channel_id = webhook_data.get('channel_id', 'webhook')
            metadata = webhook_data.get('metadata', {})
            
            if not message:
                raise ValueError("Message is required in webhook payload")

            # Process different webhook types
            if webhook_type == 'message':
                response = self.handle_message_webhook(message, user_id, source_system, channel_id, metadata)
            elif webhook_type == 'event':
                response = self.handle_event_webhook(webhook_data, user_id, source_system)
            else:
                response = self.handle_generic_webhook(webhook_data, user_id, source_system)

            processing_time = time.time() - start_time
            
            return {
                "status": "success",
                "webhook_type": webhook_type,
                "response": response,
                "user_id": user_id,
                "source_system": source_system,
                "processing_time": round(processing_time, 2),
                "timestamp": int(time.time())
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "webhook_type": webhook_data.get('type', 'unknown'),
                "processing_time": time.time() - start_time
            }

    def handle_message_webhook(self, message, user_id, source_system, channel_id, metadata):
        """Handle message-type webhooks"""
        try:
            # Call our chat API for research
            research_response = self.get_research_response(message, user_id, source_system, channel_id)
            
            # Send response to outgoing webhooks if configured
            self.trigger_outgoing_webhooks({
                "type": "research_response",
                "original_message": message,
                "response": research_response,
                "user_id": user_id,
                "source_system": source_system,
                "channel_id": channel_id,
                "metadata": metadata
            })
            
            return {
                "research_response": research_response,
                "message_processed": True
            }
            
        except Exception as e:
            print(f"Error handling message webhook: {str(e)}")
            return {"error": "Failed to process message"}

    def handle_event_webhook(self, webhook_data, user_id, source_system):
        """Handle event-type webhooks"""
        event_type = webhook_data.get('event_type', '')
        event_data = webhook_data.get('event_data', {})
        
        print(f"Received event webhook: {event_type} from {source_system}")
        
        # Process different event types
        if event_type == 'user_action':
            return {"event_processed": True, "action_logged": True}
        elif event_type == 'system_alert':
            return {"alert_received": True, "status": "acknowledged"}
        else:
            return {"event_type": event_type, "status": "received"}

    def handle_generic_webhook(self, webhook_data, user_id, source_system):
        """Handle generic webhooks"""
        print(f"Received generic webhook from {source_system}")
        
        return {
            "webhook_received": True,
            "data_keys": list(webhook_data.keys()),
            "source_system": source_system
        }

    def get_research_response(self, message, user_id, source_system, channel_id):
        """Get research response from our chat API"""
        try:
            chat_api_url = os.environ.get('CHAT_API_URL', 'https://your-vercel-app.vercel.app/api/v1/chat')
            
            payload = {
                "message": message,
                "platform": "webhook",
                "user_id": user_id,
                "channel_id": f"{source_system}_{channel_id}",
                "metadata": {
                    "source_system": source_system,
                    "webhook_type": "incoming"
                }
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': 'demo-webhook-key-abcde'
            }
            
            response = requests.post(chat_api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    return result.get('response', '')
            
            return "Research service is currently unavailable."
            
        except Exception as e:
            print(f"Error getting research response: {str(e)}")
            return "Failed to process research request."

    def trigger_outgoing_webhooks(self, data):
        """Trigger configured outgoing webhooks"""
        try:
            # In production, get outgoing webhook URLs from database
            outgoing_webhooks = os.environ.get('OUTGOING_WEBHOOK_URLS', '').split(',')
            
            for webhook_url in outgoing_webhooks:
                if webhook_url.strip():
                    self.send_outgoing_webhook(webhook_url.strip(), data)
                    
        except Exception as e:
            print(f"Error triggering outgoing webhooks: {str(e)}")

    def send_outgoing_webhook(self, webhook_url, data):
        """Send data to outgoing webhook"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'AI-Research-Assistant-Webhook/1.0'
            }
            
            # Add timestamp
            data['webhook_timestamp'] = int(time.time())
            
            response = requests.post(webhook_url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"Outgoing webhook sent successfully to {webhook_url}")
            else:
                print(f"Outgoing webhook failed: {response.status_code}")
                
        except Exception as e:
            print(f"Error sending outgoing webhook to {webhook_url}: {str(e)}")

    def log_webhook_usage(self, api_key, webhook_type):
        """Log webhook usage for analytics"""
        print(f"Webhook Usage: {api_key[:10]}... type={webhook_type} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

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
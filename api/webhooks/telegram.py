from http.server import BaseHTTPRequestHandler
import json
import os
import time
import requests
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle incoming Telegram webhook"""
        try:
            # CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Get request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                webhook_data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                print("Invalid JSON in Telegram webhook")
                return

            # Process Telegram webhook
            self.process_telegram_webhook(webhook_data)
            
            # Send 200 OK response
            response = {"status": "success"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"Error processing Telegram webhook: {str(e)}")
            self.send_response(500)
            self.end_headers()

    def process_telegram_webhook(self, webhook_data):
        """Process incoming Telegram update"""
        try:
            # Handle regular messages
            if 'message' in webhook_data:
                message = webhook_data['message']
                self.handle_telegram_message(message)
            
            # Handle callback queries (inline buttons)
            elif 'callback_query' in webhook_data:
                callback_query = webhook_data['callback_query']
                self.handle_telegram_callback(callback_query)
                
            # Handle inline queries
            elif 'inline_query' in webhook_data:
                inline_query = webhook_data['inline_query']
                self.handle_telegram_inline_query(inline_query)

        except Exception as e:
            print(f"Error processing Telegram update: {str(e)}")

    def handle_telegram_message(self, message):
        """Handle individual Telegram message"""
        try:
            user = message.get('from', {})
            chat = message.get('chat', {})
            text = message.get('text', '')
            message_id = message.get('message_id', '')
            
            user_id = user.get('id', '')
            username = user.get('username', 'Unknown')
            chat_id = chat.get('id', '')
            chat_type = chat.get('type', 'private')
            
            if not text:
                return

            print(f"Telegram message from @{username} ({user_id}): {text}")

            # Handle commands
            if text.startswith('/'):
                self.handle_telegram_command(text, chat_id, user_id, username)
                return

            # Handle regular research queries
            # Send typing indicator
            self.send_telegram_chat_action(chat_id, 'typing')
            
            # Get research response
            research_response = self.get_research_response(text, user_id, chat_id)
            
            # Send response
            if research_response:
                self.send_telegram_message(chat_id, research_response, parse_mode='Markdown')

        except Exception as e:
            print(f"Error handling Telegram message: {str(e)}")

    def handle_telegram_command(self, command, chat_id, user_id, username):
        """Handle Telegram bot commands"""
        try:
            if command.startswith('/start'):
                welcome_message = f"""🤖 *Welcome to AI Research Assistant!*

Hello @{username}! I'm your AI-powered research assistant. I can help you with:

📚 *Research queries* - Ask me anything and I'll provide comprehensive, well-researched answers
🔍 *Analysis* - I can analyze topics from multiple perspectives
📊 *Summaries* - Get concise summaries of complex topics

*How to use:*
• Just send me any question or topic
• Use /research <question> for specific research
• Use /help for more commands

Try asking: "What are the latest developments in AI?"
"""
                self.send_telegram_message(chat_id, welcome_message, parse_mode='Markdown')
                
            elif command.startswith('/help'):
                help_message = """📖 *Available Commands:*

/start - Welcome message and introduction
/help - Show this help message
/research <question> - Research a specific topic
/about - About this bot

*Examples:*
• `/research quantum computing applications`
• `What is machine learning?`
• `Explain blockchain technology`

Just send me any question and I'll research it for you! 🚀"""
                self.send_telegram_message(chat_id, help_message, parse_mode='Markdown')
                
            elif command.startswith('/about'):
                about_message = """🤖 *AI Research Assistant*

This bot uses advanced AI to provide comprehensive research on any topic. It searches multiple sources, analyzes information, and provides well-structured responses.

*Features:*
• Deep research capabilities
• Multiple source analysis
• Structured responses
• Real-time processing

Built with ❤️ using LangGraph and deployed on Vercel.
"""
                self.send_telegram_message(chat_id, about_message, parse_mode='Markdown')
                
            elif command.startswith('/research'):
                # Extract research query
                query = command.replace('/research', '').strip()
                if query:
                    self.send_telegram_chat_action(chat_id, 'typing')
                    research_response = self.get_research_response(query, user_id, chat_id)
                    if research_response:
                        self.send_telegram_message(chat_id, research_response, parse_mode='Markdown')
                else:
                    self.send_telegram_message(chat_id, "Please provide a question after /research\n\nExample: `/research artificial intelligence trends`", parse_mode='Markdown')
                    
        except Exception as e:
            print(f"Error handling Telegram command: {str(e)}")

    def handle_telegram_callback(self, callback_query):
        """Handle Telegram callback queries from inline buttons"""
        try:
            data = callback_query.get('data', '')
            message = callback_query.get('message', {})
            chat_id = message.get('chat', {}).get('id', '')
            
            # Answer the callback query
            self.answer_telegram_callback_query(callback_query.get('id', ''))
            
            # Handle different callback actions
            if data.startswith('research_'):
                topic = data.replace('research_', '').replace('_', ' ')
                self.send_telegram_chat_action(chat_id, 'typing')
                response = self.get_research_response(topic, callback_query.get('from', {}).get('id', ''), chat_id)
                if response:
                    self.send_telegram_message(chat_id, response, parse_mode='Markdown')
                    
        except Exception as e:
            print(f"Error handling Telegram callback: {str(e)}")

    def handle_telegram_inline_query(self, inline_query):
        """Handle Telegram inline queries"""
        try:
            query_id = inline_query.get('id', '')
            query_text = inline_query.get('query', '')
            
            if not query_text:
                return
                
            # Create inline results
            results = [
                {
                    "type": "article",
                    "id": "research_1",
                    "title": f"Research: {query_text}",
                    "description": "Get comprehensive research on this topic",
                    "input_message_content": {
                        "message_text": f"🔍 Researching: {query_text}",
                        "parse_mode": "Markdown"
                    }
                }
            ]
            
            self.answer_telegram_inline_query(query_id, results)
            
        except Exception as e:
            print(f"Error handling Telegram inline query: {str(e)}")

    def get_research_response(self, message, user_id, chat_id):
        """Get research response from our chat API"""
        try:
            chat_api_url = os.environ.get('CHAT_API_URL', 'https://your-vercel-app.vercel.app/api/v1/chat')
            
            payload = {
                "message": message,
                "platform": "telegram",
                "user_id": str(user_id),
                "channel_id": str(chat_id)
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': 'demo-telegram-key-67890'  # Use your API key
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

    def send_telegram_message(self, chat_id, text, parse_mode=None, reply_markup=None):
        """Send message via Telegram Bot API"""
        try:
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
            if not bot_token:
                print("Telegram bot token not configured")
                return False

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            # Telegram message limit is 4096 characters
            max_length = 4090  # Leave some buffer
            
            if len(text) > max_length:
                # Split message into chunks
                chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
                for i, chunk in enumerate(chunks):
                    if i > 0:
                        chunk = f"({i+1}/{len(chunks)})\n\n{chunk}"
                    self.send_single_telegram_message(url, chat_id, chunk, parse_mode, reply_markup if i == 0 else None)
            else:
                self.send_single_telegram_message(url, chat_id, text, parse_mode, reply_markup)
                
            return True
            
        except Exception as e:
            print(f"Error sending Telegram message: {str(e)}")
            return False

    def send_single_telegram_message(self, url, chat_id, text, parse_mode=None, reply_markup=None):
        """Send a single Telegram message"""
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        
        if parse_mode:
            payload["parse_mode"] = parse_mode
            
        if reply_markup:
            payload["reply_markup"] = reply_markup
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"Telegram message sent successfully to {chat_id}")
        else:
            print(f"Failed to send Telegram message: {response.status_code} - {response.text}")

    def send_telegram_chat_action(self, chat_id, action):
        """Send chat action (typing indicator)"""
        try:
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
            if not bot_token:
                return

            url = f"https://api.telegram.org/bot{bot_token}/sendChatAction"
            payload = {
                "chat_id": chat_id,
                "action": action
            }
            
            requests.post(url, json=payload)
            
        except Exception as e:
            print(f"Error sending chat action: {str(e)}")

    def answer_telegram_callback_query(self, callback_query_id, text="", show_alert=False):
        """Answer callback query"""
        try:
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
            if not bot_token:
                return

            url = f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery"
            payload = {
                "callback_query_id": callback_query_id,
                "text": text,
                "show_alert": show_alert
            }
            
            requests.post(url, json=payload)
            
        except Exception as e:
            print(f"Error answering callback query: {str(e)}")

    def answer_telegram_inline_query(self, query_id, results):
        """Answer inline query"""
        try:
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
            if not bot_token:
                return

            url = f"https://api.telegram.org/bot{bot_token}/answerInlineQuery"
            payload = {
                "inline_query_id": query_id,
                "results": results
            }
            
            requests.post(url, json=payload)
            
        except Exception as e:
            print(f"Error answering inline query: {str(e)}")

    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers() 
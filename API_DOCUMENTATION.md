# 🚀 AI Research Assistant API Documentation

## 📡 **API Endpoints Overview**

The AI Research Assistant provides multiple API endpoints for integrating with WhatsApp, Telegram, and custom webhook systems.

### **Base URL**
```
https://your-vercel-app.vercel.app/api/
```

---

## 🔑 **Authentication**

All API endpoints require authentication via API key:

```http
X-API-Key: your_api_key_here
```

Or as Bearer token:
```http
Authorization: Bearer your_api_key_here
```

### **Demo API Keys**
For testing purposes, you can use these demo keys:
- WhatsApp: `demo-whatsapp-key-12345`
- Telegram: `demo-telegram-key-67890`
- Webhook: `demo-webhook-key-abcde`

---

## 💬 **Chat API** - `/v1/chat`

Main API endpoint for getting research responses from external platforms.

### **POST** `/api/v1/chat`

#### **Request Headers**
```http
Content-Type: application/json
X-API-Key: your_api_key_here
```

#### **Request Body**
```json
{
  "message": "What are the latest developments in AI?",
  "platform": "whatsapp",
  "user_id": "user_12345",
  "channel_id": "channel_abc",
  "context": {
    "thread_id": "optional",
    "reply_to": "optional"
  }
}
```

#### **Response**
```json
{
  "status": "success",
  "response": "# Research Results for: \"What are the latest developments in AI?\"\n\nBased on my analysis...",
  "platform": "whatsapp",
  "user_id": "user_12345",
  "channel_id": "channel_abc",
  "processing_time": 2.3,
  "timestamp": 1703123456,
  "tokens_estimated": 850
}
```

#### **Platform-Specific Formatting**
- **WhatsApp**: Simple text, no markdown, bullet points preserved
- **Telegram**: Markdown support, formatted headers
- **Discord**: Full markdown support
- **Webhook**: Complete markdown with all formatting

---

## 📱 **WhatsApp Integration** - `/webhooks/whatsapp`

### **Setup WhatsApp Business API**

1. **Create Facebook App**
   - Go to [Facebook Developers](https://developers.facebook.com/)
   - Create new app with WhatsApp product

2. **Configure Webhook**
   ```
   Webhook URL: https://your-vercel-app.vercel.app/api/webhooks/whatsapp
   Verify Token: your_verify_token_here
   ```

3. **Environment Variables**
   ```bash
   WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token
   WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
   WHATSAPP_APP_SECRET=your_app_secret
   WHATSAPP_VERIFY_TOKEN=your_verify_token
   ```

### **GET** `/api/webhooks/whatsapp` - Webhook Verification
Automatically handles WhatsApp webhook verification.

### **POST** `/api/webhooks/whatsapp` - Receive Messages

#### **Webhook Payload (from WhatsApp)**
```json
{
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messages": [
              {
                "from": "1234567890",
                "id": "wamid.xxx",
                "timestamp": "1703123456",
                "text": {
                  "body": "What is machine learning?"
                },
                "type": "text"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

#### **Automatic Response**
The webhook automatically:
1. Receives WhatsApp message
2. Calls chat API for research response
3. Sends formatted response back to WhatsApp
4. Handles message length limits (4096 chars)

---

## 🤖 **Telegram Integration** - `/webhooks/telegram`

### **Setup Telegram Bot**

1. **Create Bot with BotFather**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Use `/newbot` command
   - Get bot token

2. **Set Webhook**
   ```bash
   curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
        -H "Content-Type: application/json" \
        -d '{
          "url": "https://your-vercel-app.vercel.app/api/webhooks/telegram"
        }'
   ```

3. **Environment Variables**
   ```bash
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

### **POST** `/api/webhooks/telegram` - Receive Updates

#### **Webhook Payload (from Telegram)**
```json
{
  "update_id": 123456789,
  "message": {
    "message_id": 123,
    "from": {
      "id": 987654321,
      "username": "user123",
      "first_name": "John"
    },
    "chat": {
      "id": 987654321,
      "type": "private"
    },
    "date": 1703123456,
    "text": "What is quantum computing?"
  }
}
```

#### **Supported Commands**
- `/start` - Welcome message
- `/help` - Show available commands
- `/research <question>` - Research specific topic
- `/about` - About the bot
- Regular messages are automatically processed as research queries

#### **Features**
- Markdown formatting support
- Typing indicators
- Message length handling (4096 chars)
- Inline queries support
- Callback button handling

---

## 🔗 **Custom Webhook Integration** - `/webhooks/incoming`

For connecting your own systems and applications.

### **POST** `/api/webhooks/incoming`

#### **Request Headers**
```http
Content-Type: application/json
X-API-Key: your_api_key_here
X-Webhook-Signature: sha256=signature_hash (optional)
```

#### **Message Webhook**
```json
{
  "type": "message",
  "message": "Research the latest trends in renewable energy",
  "user_id": "user_123",
  "source_system": "your_app_name",
  "channel_id": "support_channel",
  "metadata": {
    "priority": "high",
    "department": "research"
  }
}
```

#### **Event Webhook**
```json
{
  "type": "event",
  "event_type": "user_action",
  "event_data": {
    "action": "research_requested",
    "topic": "artificial intelligence"
  },
  "user_id": "user_123",
  "source_system": "your_app_name"
}
```

#### **Response**
```json
{
  "status": "success",
  "webhook_type": "message",
  "response": {
    "research_response": "# Renewable Energy Trends...",
    "message_processed": true
  },
  "user_id": "user_123",
  "source_system": "your_app_name",
  "processing_time": 1.8,
  "timestamp": 1703123456
}
```

### **Outgoing Webhooks**

Configure outgoing webhooks to receive research responses:

#### **Environment Variable**
```bash
OUTGOING_WEBHOOK_URLS=https://your-app.com/webhook1,https://your-app.com/webhook2
```

#### **Outgoing Payload**
```json
{
  "type": "research_response",
  "original_message": "What is blockchain?",
  "response": "# Blockchain Technology...",
  "user_id": "user_123",
  "source_system": "your_app",
  "channel_id": "general",
  "webhook_timestamp": 1703123456,
  "metadata": {
    "priority": "high"
  }
}
```

---

## 🔒 **Security Features**

### **API Key Validation**
All endpoints validate API keys before processing requests.

### **Webhook Signature Verification**
Optional webhook signature verification using HMAC-SHA256:

```python
import hmac
import hashlib

def verify_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    return signature == f'sha256={expected}'
```

### **Rate Limiting**
- Per-API-key rate limiting (configurable)
- Platform-specific limits
- Burst protection for traffic spikes

---

## 📊 **Usage Analytics**

All API calls are logged with:
- API key usage
- Platform statistics
- Processing times
- Error rates
- Message volumes

---

## 🛠 **Error Handling**

### **Common Error Responses**

#### **401 Unauthorized**
```json
{
  "status": "error",
  "error": "Invalid or missing API key",
  "timestamp": 1703123456
}
```

#### **400 Bad Request**
```json
{
  "status": "error",
  "error": "Invalid JSON format",
  "timestamp": 1703123456
}
```

#### **429 Rate Limited**
```json
{
  "status": "error",
  "error": "Rate limit exceeded",
  "timestamp": 1703123456
}
```

#### **500 Internal Server Error**
```json
{
  "status": "error",
  "error": "Internal server error",
  "timestamp": 1703123456
}
```

---

## 📋 **Integration Examples**

### **cURL Examples**

#### **Chat API**
```bash
curl -X POST "https://your-vercel-app.vercel.app/api/v1/chat" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: demo-webhook-key-abcde" \
     -d '{
       "message": "What is artificial intelligence?",
       "platform": "webhook",
       "user_id": "test_user",
       "channel_id": "test_channel"
     }'
```

#### **Custom Webhook**
```bash
curl -X POST "https://your-vercel-app.vercel.app/api/webhooks/incoming" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: demo-webhook-key-abcde" \
     -d '{
       "type": "message",
       "message": "Research quantum computing applications",
       "user_id": "research_team",
       "source_system": "research_portal",
       "channel_id": "quantum_channel"
     }'
```

### **JavaScript/Node.js Example**
```javascript
const axios = require('axios');

async function getResearchResponse(message) {
  try {
    const response = await axios.post(
      'https://your-vercel-app.vercel.app/api/v1/chat',
      {
        message: message,
        platform: 'webhook',
        user_id: 'js_user',
        channel_id: 'web_app'
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'demo-webhook-key-abcde'
        }
      }
    );
    
    return response.data.response;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    return null;
  }
}

// Usage
getResearchResponse('What are the benefits of renewable energy?')
  .then(response => console.log(response));
```

### **Python Example**
```python
import requests
import json

def get_research_response(message, platform='webhook'):
    url = 'https://your-vercel-app.vercel.app/api/v1/chat'
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': 'demo-webhook-key-abcde'
    }
    
    payload = {
        'message': message,
        'platform': platform,
        'user_id': 'python_user',
        'channel_id': 'python_app'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get('status') == 'success':
            return result.get('response')
        else:
            print(f"API Error: {result.get('error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None

# Usage
response = get_research_response('Explain machine learning algorithms')
if response:
    print(response)
```

---

## 🌟 **Next Steps**

1. **Get API Keys**: Contact support to get production API keys
2. **Test Integration**: Use demo keys to test your integration
3. **Configure Webhooks**: Set up your webhook endpoints
4. **Monitor Usage**: Track API usage and performance
5. **Scale Up**: Increase rate limits as needed

---

## 📞 **Support**

- **Documentation**: This guide
- **Issues**: GitHub Issues
- **Community**: Discord Server
- **Email**: support@ai-research-assistant.com

**Built with ❤️ using Vercel Serverless Functions, WhatsApp Business API, Telegram Bot API, and LangGraph** 
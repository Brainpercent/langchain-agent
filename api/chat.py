from flask import Flask, request, jsonify
import json
import os
import time

def handler(request):
    """Simple chat API handler for Vercel"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key',
            'Access-Control-Max-Age': '86400',
        }
        return ('', 200, headers)
    
    # Only allow POST
    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        message = data.get('message', '')
        platform = data.get('platform', 'web')
        user_id = data.get('user_id', 'anonymous')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Generate demo response
        demo_response = f"""# Research Analysis: "{message}"

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
*Powered by Deep Research AI*"""
        
        response_data = {
            "status": "success",
            "response": demo_response,
            "platform": platform,
            "user_id": user_id,
            "processing_time": 2.5,
            "timestamp": int(time.time())
        }
        
        # Set CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key',
        }
        
        return (jsonify(response_data), 200, headers)
        
    except Exception as e:
        error_response = {
            "status": "error",
            "error": f"Internal server error: {str(e)}",
            "timestamp": int(time.time())
        }
        
        headers = {'Access-Control-Allow-Origin': '*'}
        return (jsonify(error_response), 500, headers) 
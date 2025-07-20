#!/usr/bin/env python3
"""
Simple test script for the modern implementation
"""

import requests
import json

def test_modern():
    print("🧪 Testing modern implementation...")
    
    data = {
        "input": {
            "messages": [
                {"role": "user", "content": "Brief overview of artificial intelligence"}
            ]
        },
        "config": {
            "configurable": {
                "thread_id": "test_123",
                "search_api": "tavily",  # Use tavily search
                "research_model": "openai:gpt-4.1",
                "final_report_model": "openai:gpt-4.1",
                "summarization_model": "openai:gpt-4.1-nano",
                "compression_model": "openai:gpt-4.1-mini",
                "max_concurrent_research_units": 1,
                "max_researcher_iterations": 1,
                "allow_clarification": False,
                "max_react_tool_calls": 3
            }
        },
        "implementation": "modern"
    }
    
    try:
        print("📤 Sending request...")
        response = requests.post(
            "http://localhost:8000/invoke",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Response keys: {list(result.keys())}")
            if 'output' in result:
                output = result['output']
                print(f"Output keys: {list(output.keys()) if isinstance(output, dict) else 'non-dict'}")
                if 'final_report' in output:
                    print(f"Final report length: {len(output['final_report'])} chars")
                    if output['final_report']:
                        print(f"Final report preview: {output['final_report'][:200]}...")
                    else:
                        print("⚠️ Final report is empty")
                
                if 'research_brief' in output:
                    print(f"Research brief: {output['research_brief'][:100]}..." if output['research_brief'] else "Research brief is empty")
                
                if 'notes' in output:
                    print(f"Notes count: {len(output['notes']) if output['notes'] else 0}")
                
                if 'messages' in output:
                    print(f"Messages count: {len(output['messages']) if output['messages'] else 0}")
                    if output['messages']:
                        last_msg = output['messages'][-1]
                        if hasattr(last_msg, 'content'):
                            print(f"Last message preview: {str(last_msg.content)[:100]}...")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error text: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    test_modern() 
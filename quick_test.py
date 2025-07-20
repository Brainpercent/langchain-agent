#!/usr/bin/env python3
"""
Quick test script with minimal configuration
"""

import requests
import json
import time

def quick_test():
    print("🚀 Quick test of modern implementation...")
    
    data = {
        "input": {
            "messages": [
                {"role": "user", "content": "Quick summary of machine learning"}
            ]
        },
        "config": {
            "configurable": {
                "thread_id": f"quick_test_{int(time.time())}",
                "search_api": "none",  # No search for faster testing
                "research_model": "openai:gpt-4.1-mini",  # Use mini for speed
                "final_report_model": "openai:gpt-4.1-mini",
                "summarization_model": "openai:gpt-4.1-nano",
                "compression_model": "openai:gpt-4.1-mini",
                "max_concurrent_research_units": 1,
                "max_researcher_iterations": 1,
                "allow_clarification": False,
                "max_react_tool_calls": 1
            }
        },
        "implementation": "modern"
    }
    
    try:
        print("📤 Sending quick test request...")
        response = requests.post(
            "http://localhost:8000/invoke",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30  # Shorter timeout
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            output = result.get('output', {})
            
            print(f"Research brief: {len(output.get('research_brief', ''))} chars")
            print(f"Final report: {len(output.get('final_report', ''))} chars")
            print(f"Notes: {len(output.get('notes', []))}")
            
            if output.get('final_report'):
                print(f"Final report preview:\n{output['final_report'][:300]}...")
            elif output.get('research_brief'):
                print(f"Research brief: {output['research_brief'][:200]}...")
            else:
                print("⚠️ No content generated")
                print(f"Available keys: {list(output.keys())}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"Error text: {response.text[:300]}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out (30s) - workflow might be running longer")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    quick_test() 
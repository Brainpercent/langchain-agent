#!/usr/bin/env python3
"""
Test script to verify LangGraph Deep Research integration

This script tests all three implementations to ensure they work properly.
"""

import os
import sys
import json
import asyncio
import requests
import time
from pathlib import Path

def check_environment():
    """Check if environment is properly configured."""
    print("🔧 Checking environment configuration...")
    
    required_vars = ['OPENAI_API_KEY', 'TAVILY_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    print("✅ Environment variables configured")
    return True

def check_backend_structure():
    """Check if backend structure exists."""
    print("📁 Checking backend structure...")
    
    backend_path = Path("backend_temp/src")
    if not backend_path.exists():
        print(f"❌ Backend directory not found: {backend_path}")
        return False
    
    # Check modern implementation
    modern_files = [
        "open_deep_research/deep_researcher.py",
        "open_deep_research/configuration.py", 
        "open_deep_research/state.py",
        "open_deep_research/utils.py",
        "open_deep_research/prompts.py"
    ]
    
    missing_modern = []
    for file_path in modern_files:
        if not (backend_path / file_path).exists():
            missing_modern.append(file_path)
    
    if missing_modern:
        print(f"⚠️ Modern implementation missing files: {missing_modern}")
    else:
        print("✅ Modern implementation files found")
    
    # Check legacy implementations
    legacy_files = ["legacy/graph.py", "legacy/multi_agent.py"]
    legacy_found = []
    
    for file_path in legacy_files:
        if (backend_path / file_path).exists():
            legacy_found.append(file_path.split('/')[-1])
    
    if legacy_found:
        print(f"✅ Legacy implementations found: {legacy_found}")
    else:
        print("⚠️ No legacy implementations found")
    
    return len(missing_modern) == 0 or len(legacy_found) > 0

def test_server_health():
    """Test if the server is running and healthy."""
    print("🔬 Testing server health...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Server is healthy")
            print(f"📊 Available implementations: {health_data.get('available_implementations', [])}")
            return health_data
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure to start the server with: python server.py")
        return None

def test_implementation(implementation, test_query="Overview of Model Context Protocol"):
    """Test a specific implementation."""
    print(f"🧪 Testing {implementation} implementation...")
    
    # Prepare request based on implementation
    if implementation == "modern":
        request_data = {
            "input": {
                "messages": [
                    {"role": "user", "content": test_query}
                ]
            },
            "config": {
                "configurable": {
                    "thread_id": f"test_{implementation}_{int(time.time())}",
                    "search_api": "tavily",
                    "research_model": "openai:gpt-4.1-mini",  # Use mini for faster testing
                    "final_report_model": "openai:gpt-4.1-mini",
                    "summarization_model": "openai:gpt-4.1-nano",
                    "compression_model": "openai:gpt-4.1-mini",
                    "max_concurrent_research_units": 2,  # Reduced for testing
                    "max_researcher_iterations": 2,
                    "allow_clarification": False,
                    "max_react_tool_calls": 3
                }
            },
            "implementation": implementation
        }
    elif implementation == "graph":
        request_data = {
            "input": {
                "topic": test_query
            },
            "config": {
                "configurable": {
                    "thread_id": f"test_{implementation}_{int(time.time())}",
                    "search_api": "tavily",
                    "planner_provider": "openai",
                    "planner_model": "gpt-4o-mini",
                    "writer_provider": "openai",
                    "writer_model": "gpt-4o-mini",
                    "max_search_depth": 1,  # Reduced for testing
                    "auto_approve": True
                }
            },
            "implementation": implementation
        }
    elif implementation == "multi_agent":
        request_data = {
            "input": {
                "messages": [
                    {"role": "user", "content": test_query}
                ]
            },
            "config": {
                "configurable": {
                    "thread_id": f"test_{implementation}_{int(time.time())}",
                    "search_api": "tavily",
                    "supervisor_model": "gpt-4o-mini",
                    "researcher_model": "gpt-4o-mini",
                    "number_of_queries": 2,  # Reduced for testing
                    "ask_for_clarification": False
                }
            },
            "implementation": implementation
        }
    
    try:
        print(f"📤 Sending request to {implementation} implementation...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8000/invoke",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=120  # 2 minutes timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {implementation} test successful ({duration:.1f}s)")
            
            # Check response structure
            if "output" in result:
                output = result["output"]
                
                # Check for report content
                report_found = False
                if "final_report" in output and output["final_report"]:
                    print(f"📝 Final report generated ({len(output['final_report'])} chars)")
                    report_found = True
                elif "content" in output and output["content"]:
                    print(f"📝 Content generated ({len(output['content'])} chars)")
                    report_found = True
                elif isinstance(output, str) and output:
                    print(f"📝 Output generated ({len(output)} chars)")
                    report_found = True
                
                if report_found:
                    print(f"🎯 {implementation} implementation working correctly")
                    return True
                else:
                    print(f"⚠️ {implementation} implementation returned empty content")
                    print(f"Response keys: {list(output.keys()) if isinstance(output, dict) else 'non-dict'}")
                    return False
            else:
                print(f"⚠️ {implementation} implementation missing output field")
                print(f"Response keys: {list(result.keys())}")
                return False
        else:
            print(f"❌ {implementation} test failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"Error: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏰ {implementation} test timed out (2 minutes)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {implementation} test failed with network error: {e}")
        return False
    except Exception as e:
        print(f"❌ {implementation} test failed with error: {e}")
        return False

def test_web_interface():
    """Test the web interface API endpoint."""
    print("🌐 Testing web interface API...")
    
    try:
        # Test GET request
        response = requests.get("http://localhost:3000/api/chat", timeout=10)
        if response.status_code == 200:
            print("✅ Web interface GET endpoint working")
        else:
            print(f"⚠️ Web interface GET returned: {response.status_code}")
        
        # Test POST request
        response = requests.post(
            "http://localhost:3000/api/chat",
            json={
                "message": "Test research query",
                "implementation": "modern"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Web interface POST endpoint working")
            return True
        else:
            print(f"⚠️ Web interface POST returned: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Web interface not accessible: {e}")
        print("💡 Start the web interface with: npm run dev")
        return False

def main():
    """Main test function."""
    print("🔬 LangGraph Deep Research Integration Test")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed")
        sys.exit(1)
    
    # Check backend structure
    if not check_backend_structure():
        print("❌ Backend structure check failed")
        sys.exit(1)
    
    # Test server health
    health_data = test_server_health()
    if not health_data:
        print("❌ Server health check failed")
        sys.exit(1)
    
    available_implementations = health_data.get("available_implementations", [])
    if not available_implementations:
        print("❌ No implementations available")
        sys.exit(1)
    
    # Test each available implementation
    test_results = {}
    for impl in available_implementations:
        test_results[impl] = test_implementation(impl)
    
    # Test web interface
    web_test = test_web_interface()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    for impl, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{impl.upper()} implementation: {status}")
    
    web_status = "✅ PASS" if web_test else "⚠️ SKIP" 
    print(f"Web interface: {web_status}")
    
    successful_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    if successful_tests == total_tests:
        print(f"\n🎉 All tests passed! ({successful_tests}/{total_tests})")
        print("✅ Your LangGraph integration is working correctly")
    elif successful_tests > 0:
        print(f"\n⚠️ Partial success ({successful_tests}/{total_tests})")
        print("Some implementations are working correctly")
    else:
        print(f"\n❌ All tests failed ({successful_tests}/{total_tests})")
        print("Please check your configuration and server setup")

if __name__ == "__main__":
    main() 
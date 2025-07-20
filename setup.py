#!/usr/bin/env python3
"""
Setup script for LangGraph Deep Research API Server

This script helps you get your LangGraph research workflow running quickly.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_environment_variables():
    """Check if required environment variables are set."""
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for LLM models',
        'TAVILY_API_KEY': 'Tavily API key for web search',
        'ANTHROPIC_API_KEY': 'Anthropic API key for Claude models (optional)'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  - {var}: {description}")
    
    if missing_vars:
        print("⚠️ Missing environment variables:")
        for var in missing_vars:
            print(var)
        print("\nSet these in your environment or create a .env file:")
        print("export OPENAI_API_KEY=your_key_here")
        print("export TAVILY_API_KEY=your_key_here")
        print("export ANTHROPIC_API_KEY=your_key_here  # optional")
        return False
    
    print("✅ All required environment variables are set")
    return True

def install_requirements():
    """Install required packages."""
    try:
        print("📦 Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-server.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ requirements-server.txt not found")
        return False

def check_backend_structure():
    """Check if backend structure exists."""
    backend_path = Path("backend_temp/src")
    
    if not backend_path.exists():
        print(f"❌ Backend directory not found: {backend_path}")
        print("Please ensure you have the backend_temp/src directory with your LangGraph implementations")
        return False
    
    implementations = []
    
    # Check for modern implementation (deep_researcher)
    modern_path = backend_path / "open_deep_research"
    if modern_path.exists():
        deep_researcher_file = modern_path / "deep_researcher.py"
        if deep_researcher_file.exists():
            implementations.append("modern")
            print("✅ Modern implementation found (deep_researcher.py)")
        else:
            print("⚠️ Modern implementation directory found but deep_researcher.py missing")
            
        # Also check for other required files
        config_file = modern_path / "configuration.py"
        state_file = modern_path / "state.py"
        utils_file = modern_path / "utils.py"
        prompts_file = modern_path / "prompts.py"
        
        missing_files = []
        if not config_file.exists():
            missing_files.append("configuration.py")
        if not state_file.exists():
            missing_files.append("state.py")
        if not utils_file.exists():
            missing_files.append("utils.py")
        if not prompts_file.exists():
            missing_files.append("prompts.py")
            
        if missing_files:
            print(f"⚠️ Modern implementation missing files: {', '.join(missing_files)}")
    else:
        print("⚠️ Modern implementation (open_deep_research) not found")
    
    # Check for legacy implementations
    legacy_path = backend_path / "legacy"
    if legacy_path.exists():
        # Check for graph implementation
        graph_file = legacy_path / "graph.py"
        if graph_file.exists():
            implementations.append("graph")
            print("✅ Graph-based implementation found (legacy)")
        else:
            print("⚠️ Graph-based implementation (graph.py) not found")
        
        # Check for multi-agent implementation
        multi_agent_file = legacy_path / "multi_agent.py"
        if multi_agent_file.exists():
            implementations.append("multi_agent")
            print("✅ Multi-agent implementation found (legacy)")
        else:
            print("⚠️ Multi-agent implementation (multi_agent.py) not found")
    else:
        print("⚠️ Legacy directory not found - legacy implementations unavailable")
    
    if not implementations:
        print("❌ No implementations found")
        print("\nExpected structure:")
        print("  backend_temp/src/")
        print("    ├── open_deep_research/")
        print("    │   ├── deep_researcher.py     # Main workflow")
        print("    │   ├── configuration.py       # Config classes")
        print("    │   ├── state.py              # State definitions")
        print("    │   ├── utils.py              # Utility functions")
        print("    │   └── prompts.py            # Prompt templates")
        print("    └── legacy/")
        print("        ├── graph.py              # Graph-based workflow")
        print("        └── multi_agent.py        # Multi-agent workflow")
        return False
    
    print(f"🎯 Available implementations: {', '.join(implementations)}")
    
    # Recommend the best implementation
    if "modern" in implementations:
        print("💡 Recommended: Use 'modern' implementation (deep_researcher) for production")
    elif "multi_agent" in implementations:
        print("💡 Recommended: Use 'multi_agent' implementation for speed")
    elif "graph" in implementations:
        print("💡 Recommended: Use 'graph' implementation for quality")
    
    return True

def create_env_template():
    """Create a .env template file."""
    env_template = """# LangGraph Deep Research API Environment Variables

# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional API Keys (enhance capabilities)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_API_KEY=your_groq_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# LangGraph Server Configuration
LANGGRAPH_API_URL=http://localhost:8000

# Web Interface Configuration (for Vercel deployment)
NEXT_PUBLIC_LANGGRAPH_API_URL=http://localhost:8000

# Implementation Selection (optional - defaults to 'modern')
# RESEARCH_IMPLEMENTATION=modern  # or 'graph' or 'multi_agent'

# Modern Implementation Configuration (optional)
# RESEARCH_MODEL=openai:gpt-4
# FINAL_REPORT_MODEL=openai:gpt-4
# COMPRESSION_MODEL=openai:gpt-4-mini
# MAX_CONCURRENT_RESEARCH_UNITS=3
# MAX_RESEARCHER_ITERATIONS=3
"""
    
    try:
        with open(".env.template", "w") as f:
            f.write(env_template)
        print("✅ Created .env.template file")
        print("📝 Copy .env.template to .env and fill in your API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env.template: {e}")
        return False

def start_server():
    """Start the LangGraph server."""
    try:
        print("🚀 Starting LangGraph Deep Research API Server...")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🔬 Health Check: http://localhost:8000/health")
        print("🎯 Available Implementations: http://localhost:8000/implementations")
        print("⏹️ Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([sys.executable, "server.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    except FileNotFoundError:
        print("❌ server.py not found")
        return False

def main():
    """Main setup function."""
    print("🔬 LangGraph Deep Research API Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Check backend structure
    if not check_backend_structure():
        print("\n❌ Setup failed: Backend structure incomplete")
        print("\n💡 Setup Guide:")
        print("1. Ensure you have the correct directory structure")
        print("2. Check that implementation files exist")
        print("3. Install required dependencies")
        print("4. The modern implementation requires multiple Python files")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed: Could not install requirements")
        sys.exit(1)
    
    # Create environment template
    create_env_template()
    
    # Check environment variables
    env_ready = check_environment_variables()
    
    print("\n" + "=" * 40)
    if env_ready:
        print("✅ Setup complete! Ready to start server.")
        print("\n🎯 Implementation Features:")
        print("  • modern: Multi-stage pipeline with concurrent research units")
        print("  • graph: Sequential workflow with quality control")
        print("  • multi_agent: Parallel processing with supervisor")
        
        # Ask if user wants to start server now
        while True:
            choice = input("\n🚀 Start the server now? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                start_server()
                break
            elif choice in ['n', 'no']:
                print("\n📋 To start the server later, run: python server.py")
                print("🌐 Web interface will default to 'modern' (deep_researcher) implementation")
                break
            else:
                print("Please enter 'y' or 'n'")
    else:
        print("⚠️ Setup incomplete: Please configure environment variables")
        print("📋 After setting up .env file, run: python server.py")

if __name__ == "__main__":
    main() 
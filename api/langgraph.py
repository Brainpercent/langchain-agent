"""
Vercel API endpoint for LangGraph Deep Research integration
"""

import os
import sys
import json
from typing import Dict, Any, Optional

# Add the backend_temp/src directory to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_src = os.path.join(project_root, 'backend_temp', 'src')
sys.path.insert(0, backend_src)

def handler(request, response):
    """Vercel serverless function handler for LangGraph research workflows"""
    
    # Handle CORS
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response.status = 200
        return ''
    
    # Handle GET request - health check
    if request.method == 'GET':
        return json.dumps({
            "status": "healthy",
            "message": "🔬 LangGraph Deep Research API (Vercel)",
            "available_implementations": ["modern", "graph", "multi_agent"],
            "environment": "vercel"
        })
    
    # Handle POST request - research invocation
    if request.method == 'POST':
        try:
            # Parse request body
            if hasattr(request, 'json') and request.json:
                data = request.json
            else:
                data = json.loads(request.body) if request.body else {}
            
            # Extract parameters
            implementation = data.get('implementation', 'modern')
            research_input = data.get('input', {})
            config = data.get('config', {})
            
            # For Vercel, we'll focus on the modern implementation
            if implementation == 'modern':
                return handle_modern_research(research_input, config)
            else:
                # Fallback for other implementations
                return handle_fallback_research(research_input, implementation)
                
        except Exception as e:
            response.status = 500
            return json.dumps({
                "status": "error",
                "error": f"Server error: {str(e)}",
                "implementation": "vercel"
            })
    
    # Method not allowed
    response.status = 405
    return json.dumps({
        "status": "error",
        "error": f"Method {request.method} not allowed"
    })

def handle_modern_research(research_input: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Handle modern implementation research in Vercel environment"""
    
    try:
        # Import the modern implementation
        from open_deep_research.deep_researcher import deep_researcher_builder
        from langgraph.checkpoint.memory import MemorySaver
        import uuid
        import asyncio
        
        # Initialize memory and compile graph
        memory = MemorySaver()
        graph = deep_researcher_builder.compile(checkpointer=memory)
        
        # Set up configuration with defaults
        configurable = config.get('configurable', {})
        
        # Use provided thread_id or generate one
        thread_id = configurable.get('thread_id', str(uuid.uuid4()))
        
        # Set defaults optimized for Vercel (faster execution)
        default_config = {
            'thread_id': thread_id,
            'search_api': 'tavily',
            'research_model': 'openai:gpt-4.1-mini',  # Use mini for speed
            'final_report_model': 'openai:gpt-4.1-mini',
            'summarization_model': 'openai:gpt-4.1-nano',
            'compression_model': 'openai:gpt-4.1-mini',
            'max_concurrent_research_units': 1,  # Reduce for Vercel
            'max_researcher_iterations': 1,  # Reduce for Vercel
            'allow_clarification': False,
            'max_react_tool_calls': 2  # Reduce for Vercel
        }
        
        # Update with provided config
        for key, value in configurable.items():
            default_config[key] = value
        
        graph_config = {'configurable': default_config}
        
        # Ensure proper input format
        if 'messages' not in research_input and 'topic' in research_input:
            research_input['messages'] = [{"role": "user", "content": research_input['topic']}]
        
        # Run the async workflow
        result = asyncio.run(run_research_workflow(graph, research_input, graph_config))
        
        return json.dumps({
            "status": "success",
            "output": result,
            "implementation": "modern",
            "thread_id": thread_id,
            "environment": "vercel"
        })
        
    except ImportError as e:
        # Fallback if modern implementation not available
        return handle_fallback_research(research_input, 'modern', f"Modern implementation not available: {e}")
    except Exception as e:
        return json.dumps({
            "status": "error", 
            "error": f"Modern research failed: {str(e)}",
            "implementation": "modern"
        })

async def run_research_workflow(graph, research_input, graph_config):
    """Run the research workflow asynchronously"""
    
    final_state = None
    
    # Stream through the workflow
    async for event in graph.astream(research_input, graph_config, stream_mode="updates"):
        final_state = event
        
        # Handle clarification requests (auto-skip for Vercel)
        if 'messages' in event and event['messages']:
            last_message = event['messages'][-1]
            if hasattr(last_message, 'content') and 'clarification' in str(last_message.content).lower():
                continue  # Skip clarification
    
    # Get final state if needed
    if not final_state:
        state = graph.get_state(graph_config)
        final_state = state.values
    
    # Extract structured result
    if isinstance(final_state, dict):
        return {
            "final_report": final_state.get("final_report", ""),
            "research_brief": final_state.get("research_brief", ""),
            "notes": final_state.get("notes", []),
            "messages": final_state.get("messages", [])
        }
    else:
        return {"content": str(final_state)}

def handle_fallback_research(research_input: Dict[str, Any], implementation: str, error_msg: str = None) -> str:
    """Handle fallback research using OpenAI directly"""
    
    try:
        import openai
        
        # Get the research topic
        if 'messages' in research_input and research_input['messages']:
            topic = research_input['messages'][-1].get('content', 'Research topic')
        elif 'topic' in research_input:
            topic = research_input['topic']
        else:
            topic = 'General research query'
        
        # Use OpenAI for fallback research
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            return json.dumps({
                "status": "error",
                "error": "OpenAI API key not configured for fallback",
                "implementation": f"{implementation}_fallback"
            })
        
        client = openai.OpenAI(api_key=openai_key)
        
        # Generate research-style response
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use available model
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are a sophisticated research assistant that mimics the LangGraph deep research workflow.
                    
Implementation type: {implementation}
{error_msg or f"Running in Vercel serverless fallback mode for {implementation} implementation."}

Create a comprehensive research report on the user's topic with:
1. Executive summary
2. Detailed analysis with multiple sections
3. Key findings and insights  
4. Strategic recommendations
5. Professional markdown formatting

Make this a thorough, well-structured research report."""
                },
                {"role": "user", "content": f"Conduct comprehensive research on: {topic}"}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        
        research_content = response.choices[0].message.content
        
        return json.dumps({
            "status": "success",
            "output": {
                "final_report": research_content,
                "research_brief": f"Research analysis of: {topic}",
                "notes": [f"Generated using OpenAI fallback in Vercel environment"],
                "messages": []
            },
            "implementation": f"{implementation}_fallback",
            "environment": "vercel"
        })
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": f"Fallback research failed: {str(e)}",
            "implementation": f"{implementation}_fallback"
        }) 
#!/usr/bin/env python3
"""
FastAPI server for LangGraph Deep Research Agent

This server exposes multiple LangGraph research workflows as REST APIs:
- Modern implementation (open_deep_research.deep_researcher)
- Graph-based workflow (legacy.graph) 
- Multi-agent workflow (legacy.multi_agent)
"""

import os
import sys
import uuid
import asyncio
from typing import Dict, Any, Optional, Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add the backend_temp/src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend_temp', 'src'))

# Import LangGraph components
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

# Import all available research workflow implementations
modern_builder = None
graph_builder = None
multi_agent_builder = None
AVAILABLE_IMPLEMENTATIONS = []

# Try modern implementation first
try:
    from open_deep_research.deep_researcher import deep_researcher as modern_builder
    AVAILABLE_IMPLEMENTATIONS.append("modern")
    print("✅ Modern implementation loaded (open_deep_research.deep_researcher)")
except ImportError as e:
    print(f"⚠️ Modern implementation not available: {e}")

# Try legacy implementations
try:
    from legacy.graph import builder as graph_builder
    AVAILABLE_IMPLEMENTATIONS.append("graph")
    print("✅ Graph-based implementation loaded (legacy)")
except ImportError as e:
    print(f"⚠️ Graph-based implementation not available: {e}")

try:
    from legacy.multi_agent import supervisor_builder as multi_agent_builder
    AVAILABLE_IMPLEMENTATIONS.append("multi_agent")
    print("✅ Multi-agent implementation loaded (legacy)")
except ImportError as e:
    print(f"⚠️ Multi-agent implementation not available: {e}")

if not AVAILABLE_IMPLEMENTATIONS:
    print("❌ No research implementations available")
    sys.exit(1)

# Request/Response models
class ResearchRequest(BaseModel):
    input: Dict[str, Any]
    config: Optional[Dict[str, Any]] = None
    implementation: Optional[Literal["modern", "graph", "multi_agent"]] = "modern"

class ResearchResponse(BaseModel):
    output: Dict[str, Any]
    status: str = "success"
    implementation: str
    thread_id: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph Deep Research API",
    description="API for comprehensive research reports using LangGraph workflows",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
graphs = {}
memory = None

def initialize_graphs():
    """Initialize all available research workflows with memory checkpointer."""
    global graphs, memory
    try:
        print("🔬 Initializing LangGraph research workflows...")
        memory = MemorySaver()
        
        if modern_builder and "modern" in AVAILABLE_IMPLEMENTATIONS:
            # Import the builder (not the compiled graph) and compile with checkpointer
            try:
                from open_deep_research.deep_researcher import deep_researcher_builder
                graphs["modern"] = deep_researcher_builder.compile(checkpointer=memory)
                print("✅ Modern workflow initialized (deep_researcher with checkpointer)")
            except ImportError:
                # Fallback to using the compiled version if builder not available
                graphs["modern"] = modern_builder
                print("✅ Modern workflow initialized (deep_researcher without checkpointer)")
            
        if graph_builder and "graph" in AVAILABLE_IMPLEMENTATIONS:
            graphs["graph"] = graph_builder.compile(checkpointer=memory)
            print("✅ Graph-based workflow initialized")
            
        if multi_agent_builder and "multi_agent" in AVAILABLE_IMPLEMENTATIONS:
            graphs["multi_agent"] = multi_agent_builder.compile(checkpointer=memory)
            print("✅ Multi-agent workflow initialized")
            
        print(f"🎯 Available implementations: {AVAILABLE_IMPLEMENTATIONS}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize graphs: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize the graphs on server startup."""
    if not initialize_graphs():
        print("❌ Server failed to start - could not initialize graphs")
        sys.exit(1)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "🔬 LangGraph Deep Research API is running!",
        "available_implementations": AVAILABLE_IMPLEMENTATIONS,
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "available_implementations": AVAILABLE_IMPLEMENTATIONS,
        "graphs_initialized": {impl: impl in graphs for impl in AVAILABLE_IMPLEMENTATIONS},
        "memory_enabled": memory is not None
    }

@app.post("/invoke", response_model=ResearchResponse)
async def invoke_research(request: ResearchRequest):
    """
    Invoke the LangGraph research workflow.
    
    Expected input formats:
    
    Modern implementation:
    {
        "input": {
            "messages": [{"role": "user", "content": "research topic"}]
        },
        "config": {
            "configurable": {
                "thread_id": "unique_thread_id",
                "search_api": "tavily",
                "research_model": "openai:gpt-4",
                "final_report_model": "openai:gpt-4",
                "allow_clarification": false
            }
        },
        "implementation": "modern"
    }
    
    Graph implementation:
    {
        "input": {
            "topic": "research topic here"
        },
        "config": {
            "configurable": {
                "thread_id": "unique_thread_id",
                "search_api": "tavily",
                "planner_provider": "openai",
                "planner_model": "gpt-4",
                "writer_provider": "openai", 
                "writer_model": "gpt-4",
                "auto_approve": true
            }
        },
        "implementation": "graph"
    }
    
    Multi-agent implementation:
    {
        "input": {
            "messages": [{"role": "user", "content": "topic"}]
        },
        "config": {
            "configurable": {
                "thread_id": "unique_thread_id",
                "search_api": "tavily",
                "supervisor_model": "gpt-4",
                "researcher_model": "gpt-4"
            }
        },
        "implementation": "multi_agent"
    }
    """
    
    # Validate implementation choice
    implementation = request.implementation or "modern"
    if implementation not in AVAILABLE_IMPLEMENTATIONS:
        available = ", ".join(AVAILABLE_IMPLEMENTATIONS)
        raise HTTPException(
            status_code=400, 
            detail=f"Implementation '{implementation}' not available. Available: {available}"
        )
    
    if implementation not in graphs:
        raise HTTPException(status_code=500, detail=f"Graph for '{implementation}' not initialized")
    
    try:
        # Extract input and config
        graph_input = request.input
        graph_config = request.config or {}
        
        # Ensure we have a thread_id
        if 'configurable' not in graph_config:
            graph_config['configurable'] = {}
        
        thread_id = graph_config['configurable'].get('thread_id') or str(uuid.uuid4())
        graph_config['configurable']['thread_id'] = thread_id
        
        # Set default configuration based on implementation
        if implementation == "modern":
            config_defaults = {
                'search_api': 'tavily',
                'research_model': 'openai:gpt-4.1',
                'final_report_model': 'openai:gpt-4.1',
                'summarization_model': 'openai:gpt-4.1-nano',
                'compression_model': 'openai:gpt-4.1-mini',
                'max_researcher_iterations': 3,
                'max_concurrent_research_units': 3,
                'allow_clarification': False,  # Skip clarification for web interface
                'max_react_tool_calls': 5,
                'max_structured_output_retries': 3
            }
            
            # Ensure messages format for modern implementation
            if 'messages' not in graph_input and 'topic' in graph_input:
                graph_input['messages'] = [{"role": "user", "content": graph_input['topic']}]
                
        elif implementation == "graph":
            config_defaults = {
                'search_api': 'tavily',
                'planner_provider': 'openai',
                'planner_model': 'gpt-4',
                'writer_provider': 'openai',
                'writer_model': 'gpt-4',
                'max_search_depth': 2,
                'auto_approve': True,  # Skip human feedback for web interface
                'report_structure': """Use this structure to create a comprehensive research report:

1. Introduction (no research needed)
   - Brief overview of the topic area
   - Context and scope of the research

2. Main Body Sections:
   - Each section should focus on a specific aspect of the topic
   - Include proper citations and sources
   - Provide detailed analysis and insights

3. Conclusion
   - Summary of key findings
   - Strategic recommendations
   - Next steps or implications"""
            }
            
            # Ensure topic is in input for graph implementation
            if 'topic' not in graph_input and 'messages' in graph_input:
                # Extract topic from messages if provided
                user_messages = [msg for msg in graph_input['messages'] if msg.get('role') == 'user']
                if user_messages:
                    graph_input['topic'] = user_messages[-1].get('content', 'Research topic')
            
        elif implementation == "multi_agent":
            config_defaults = {
                'search_api': 'tavily',
                'supervisor_model': 'gpt-4',
                'researcher_model': 'gpt-4',
                'number_of_queries': 3,
                'ask_for_clarification': False,  # Skip clarification for web interface
                'include_source_str': False,
            }
            
            # Ensure messages format for multi-agent implementation
            if 'messages' not in graph_input and 'topic' in graph_input:
                graph_input['messages'] = [{"role": "user", "content": graph_input['topic']}]
        
        # Apply defaults for missing config
        for key, value in config_defaults.items():
            if key not in graph_config['configurable']:
                graph_config['configurable'][key] = value
        
        print(f"🔍 Processing {implementation} research request")
        print(f"📋 Input: {graph_input}")
        print(f"🔧 Config: {graph_config['configurable']}")
        
        # Get the appropriate graph
        graph = graphs[implementation]
        
        # Handle the workflow based on implementation
        if implementation == "modern":
            # Modern implementation (deep_researcher) - runs to completion automatically
            final_state = None
            async for event in graph.astream(graph_input, graph_config, stream_mode="updates"):
                print(f"📊 Modern workflow event: {list(event.keys())}")
                final_state = event
                
                # Handle any clarification requests from the modern implementation
                if 'messages' in event and event['messages']:
                    last_message = event['messages'][-1]
                    if hasattr(last_message, 'content') and 'clarification' in str(last_message.content).lower():
                        print("ℹ️ Clarification requested but skipped for web interface")
            
            # Get final state if needed
            if not final_state:
                state = graph.get_state(graph_config)
                final_state = state.values
            
            # Extract the result from AgentState structure
            if isinstance(final_state, dict):
                # The modern implementation returns an AgentState with these key fields:
                # - final_report: The main research report
                # - messages: List of messages including the final report message
                # - research_brief: The original research question
                # - notes: Compressed research findings
                # - raw_notes: Raw research data
                result = {
                    "final_report": final_state.get("final_report", ""),
                    "research_brief": final_state.get("research_brief", ""),
                    "notes": final_state.get("notes", []),
                    "raw_notes": final_state.get("raw_notes", []),
                    "messages": final_state.get("messages", [])
                }
                
                # Ensure we have a final report
                if not result["final_report"] and result["messages"]:
                    # Try to extract from messages if final_report is empty
                    for msg in reversed(result["messages"]):
                        if hasattr(msg, 'content') and msg.content and len(str(msg.content)) > 100:
                            result["final_report"] = str(msg.content)
                            break
                
                print(f"📝 Modern implementation extracted final_report: {len(result['final_report'])} chars")
            else:
                result = {"content": str(final_state)}
                
        elif implementation == "graph" and graph_config['configurable'].get('auto_approve', False):
            # Graph-based workflow with automatic approval
            final_state = None
            
            # Stream through the workflow
            async for event in graph.astream(graph_input, graph_config, stream_mode="updates"):
                print(f"📊 Graph workflow event: {list(event.keys())}")
                
                # Handle interrupts (approval requests)
                if '__interrupt__' in event:
                    interrupt_value = event['__interrupt__'][0].value
                    print(f"⏸️ Auto-approving: {interrupt_value[:100]}...")
                    
                    # Auto-approve the plan
                    async for resume_event in graph.astream(
                        Command(resume=True), 
                        graph_config, 
                        stream_mode="updates"
                    ):
                        if '__interrupt__' not in resume_event:
                            final_state = resume_event
                    break
                else:
                    final_state = event
            
            # Get the final state
            if not final_state:
                state = graph.get_state(graph_config)
                final_state = state.values
            
            # Extract the final report
            result = {}
            if isinstance(final_state, dict):
                # Look for final_report in the state
                if 'final_report' in final_state:
                    result['final_report'] = final_state['final_report']
                elif any('final_report' in v for v in final_state.values() if isinstance(v, dict)):
                    # Search in nested values
                    for v in final_state.values():
                        if isinstance(v, dict) and 'final_report' in v:
                            result['final_report'] = v['final_report']
                            break
                else:
                    result = final_state
            else:
                result = {'content': str(final_state)}
                
        elif implementation == "multi_agent":
            # Multi-agent workflow - runs to completion automatically
            final_state = None
            async for event in graph.astream(graph_input, graph_config, stream_mode="updates"):
                print(f"📊 Multi-agent workflow event: {list(event.keys())}")
                final_state = event
            
            # Get final state if needed
            if not final_state:
                state = graph.get_state(graph_config)
                final_state = state.values
                
            result = final_state
            
        else:
            # Standard workflow with human feedback (graph implementation)
            final_state = None
            async for event in graph.astream(graph_input, graph_config, stream_mode="updates"):
                final_state = event
                if '__interrupt__' in event:
                    # Return interrupt for human feedback
                    return ResearchResponse(
                        output={
                            "interrupt": event['__interrupt__'][0].value,
                            "requires_feedback": True
                        },
                        implementation=implementation,
                        thread_id=thread_id
                    )
            
            # Get final state if no interrupts
            if not final_state:
                state = graph.get_state(graph_config)
                final_state = state.values
                
            result = final_state
        
        print(f"✅ {implementation} research completed. Result keys: {list(result.keys()) if isinstance(result, dict) else 'non-dict result'}")
        
        return ResearchResponse(
            output=result,
            implementation=implementation,
            thread_id=thread_id
        )
        
    except Exception as e:
        print(f"❌ {implementation} research workflow error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Research workflow failed: {str(e)}")

@app.post("/stream")
async def stream_research(request: ResearchRequest):
    """
    Stream the research workflow results.
    This endpoint provides real-time updates during research.
    """
    implementation = request.implementation or "modern"
    if implementation not in graphs:
        raise HTTPException(status_code=500, detail=f"Graph for '{implementation}' not initialized")
    
    # Implementation for streaming would go here
    # For now, redirect to invoke
    return await invoke_research(request)

# Additional utility endpoints

@app.get("/config/models")
async def get_available_models():
    """Get available model configurations."""
    return {
        "implementations": AVAILABLE_IMPLEMENTATIONS,
        "providers": {
            "openai": ["gpt-4.1", "gpt-4.1-nano", "gpt-4.1-mini", "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-5-sonnet-latest", "claude-3-haiku"],
            "groq": ["llama-3.3-70b-versatile", "deepseek-r1-distill-llama-70b"]
        },
        "search_apis": ["tavily", "duckduckgo", "openai", "anthropic", "none"],
        "modern_config": {
            "search_api": "tavily",
            "research_model": "openai:gpt-4.1",
            "final_report_model": "openai:gpt-4.1",
            "summarization_model": "openai:gpt-4.1-nano",
            "compression_model": "openai:gpt-4.1-mini",
            "max_researcher_iterations": 3,
            "max_concurrent_research_units": 3,
            "allow_clarification": False,
            "max_react_tool_calls": 5
        },
        "graph_config": {
            "search_api": "tavily",
            "planner_provider": "openai",
            "planner_model": "gpt-4",
            "writer_provider": "openai",
            "writer_model": "gpt-4",
            "max_search_depth": 2,
            "auto_approve": True
        },
        "multi_agent_config": {
            "search_api": "tavily",
            "supervisor_model": "gpt-4",
            "researcher_model": "gpt-4",
            "number_of_queries": 3,
            "ask_for_clarification": False
        }
    }

@app.get("/implementations")
async def get_implementations():
    """Get available research implementations and their features."""
    return {
        "available": AVAILABLE_IMPLEMENTATIONS,
        "features": {
            "modern": {
                "description": "Latest deep_researcher implementation with advanced multi-stage workflow",
                "workflow": [
                    "clarify_with_user: Understand research scope (skipped for web)",
                    "write_research_brief: Create structured research plan",
                    "research_supervisor: Coordinate concurrent research units",
                    "final_report_generation: Synthesize comprehensive report"
                ],
                "features": [
                    "Multi-stage research pipeline with supervisor coordination",
                    "Concurrent research units for parallel processing",
                    "Advanced compression and summarization models",
                    "Native web search integration (OpenAI/Anthropic)",
                    "MCP tool integration support",
                    "Configurable research iterations and tool calls",
                    "Automatic clarification bypass for web interface"
                ],
                "best_for": "Production-ready research with advanced multi-stage processing"
            },
            "graph": {
                "description": "Graph-based workflow with sequential steps and human feedback",
                "features": [
                    "Interactive planning with human approval",
                    "Sequential section writing with quality evaluation",
                    "Multiple search iterations per section",
                    "Structured report generation"
                ],
                "best_for": "High-quality reports requiring human oversight"
            },
            "multi_agent": {
                "description": "Multi-agent workflow with parallel research",
                "features": [
                    "Supervisor agent coordinating research team",
                    "Parallel section research for speed",
                    "MCP tool integration support",
                    "Automatic workflow completion"
                ],
                "best_for": "Fast research with parallel processing"
            }
        }
    }

if __name__ == "__main__":
    # Check for required environment variables
    required_env_vars = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {missing_vars}")
        print("The server will start but some features may not work properly.")
    
    print("🚀 Starting LangGraph Deep Research API Server...")
    print(f"📊 Available implementations: {AVAILABLE_IMPLEMENTATIONS}")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔬 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 
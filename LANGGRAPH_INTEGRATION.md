# 🔬 LangGraph Deep Research Integration

This guide explains how to connect your sophisticated LangGraph research workflows to the web interface, enabling users to access your AI research capabilities online.

## 🎯 Overview

Your project now supports **three powerful research implementations**:

### **Modern Implementation** (`open_deep_research/deep_researcher.py`) ⭐ **Recommended**
A sophisticated **4-stage research pipeline** with advanced AI coordination:

**Stage 1: `clarify_with_user`** - Intelligent scope assessment
- Analyzes user request for clarity and completeness
- Asks targeted clarifying questions if needed
- **Web Interface**: Auto-skipped for seamless user experience

**Stage 2: `write_research_brief`** - Strategic research planning  
- Transforms user input into detailed research objectives
- Creates comprehensive research brief with specific focus areas
- Maximizes specificity while avoiding unwarranted assumptions

**Stage 3: `research_supervisor`** - Coordinated research execution
- **Supervisor Agent**: Orchestrates up to 3 concurrent research units
- **Parallel Processing**: Each unit conducts independent deep research
- **Quality Control**: Iterative refinement until research is comprehensive
- **Tool Integration**: Web search, MCP tools, and API integration

**Stage 4: `final_report_generation`** - Professional synthesis
- Synthesizes all research findings into comprehensive reports
- Advanced compression and summarization techniques
- Professional markdown formatting with citations
- Handles token limits with intelligent content management

**Best for**: Production deployment with sophisticated research capabilities

### **Graph-Based Workflow** (`legacy/graph.py`)
- **Sequential processing** with human feedback capability
- **Interactive planning** with approval steps  
- **Quality evaluation** with multi-iteration refinement
- **Structured reports** with comprehensive citations
- **Best for**: High-quality reports requiring oversight

### **Multi-Agent Workflow** (`legacy/multi_agent.py`)
- **Supervisor-agent architecture** with parallel processing
- **Speed optimized** with concurrent research
- **MCP tool integration** for external APIs
- **Automatic completion** without human intervention
- **Best for**: Fast research with comprehensive coverage

## 🚀 Quick Start

### 1. **Setup and Installation**

Run the automated setup script:

```bash
python setup.py
```

This will:
- ✅ Check Python version compatibility
- ✅ Verify backend structure for all implementations
- ✅ Validate modern implementation files (deep_researcher.py, configuration.py, state.py, utils.py, prompts.py)
- ✅ Install required packages
- ✅ Create environment template
- ✅ Check API key configuration
- ✅ Recommend best implementation for your setup

### 2. **Configure Environment Variables**

Copy the template and add your API keys:

```bash
cp .env.template .env
```

Edit `.env` with your keys:

```env
# Required for all implementations
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional (for enhanced capabilities)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Server configuration
LANGGRAPH_API_URL=http://localhost:8000

# Modern Implementation Tuning (optional)
RESEARCH_MODEL=openai:gpt-4
FINAL_REPORT_MODEL=openai:gpt-4
COMPRESSION_MODEL=openai:gpt-4-mini
MAX_CONCURRENT_RESEARCH_UNITS=3
MAX_RESEARCHER_ITERATIONS=3
```

### 3. **Start the LangGraph Server**

```bash
python server.py
```

The server provides:
- 📚 **API Documentation**: http://localhost:8000/docs
- 🔬 **Health Check**: http://localhost:8000/health
- 🎯 **Research Endpoint**: http://localhost:8000/invoke
- 📊 **Implementation Info**: http://localhost:8000/implementations

### 4. **Connect Web Interface**

Set the environment variable for your web interface:

```bash
# For local development
export LANGGRAPH_API_URL=http://localhost:8000

# For Vercel deployment
LANGGRAPH_API_URL=http://localhost:8000
```

## 📊 Deep Researcher Workflow Details

### **Stage-by-Stage Process**

**🔍 Stage 1: Clarification (`clarify_with_user`)**
```
Input: User messages
Process: 
- Analyzes conversation history for completeness
- Identifies missing critical information or unclear terms
- Generates targeted clarifying questions if needed
- Web interface: Automatically bypassed for seamless UX
Output: Verified research readiness or clarification request
```

**📋 Stage 2: Research Brief (`write_research_brief`)**
```
Input: Clarified user request
Process:
- Transforms messages into detailed research objectives
- Maximizes specificity while preserving user intent
- Identifies research dimensions and scope
- Creates structured research plan
Output: Comprehensive research brief for supervisor
```

**🔬 Stage 3: Research Execution (`research_supervisor`)**
```
Input: Research brief
Process:
- Supervisor coordinates up to 3 concurrent research units
- Each unit conducts independent deep research on specific topics
- Parallel processing with quality checkpoints
- Iterative refinement until comprehensive coverage achieved
- Integration with web search APIs and MCP tools
Output: Comprehensive research findings and raw notes
```

**📝 Stage 4: Report Generation (`final_report_generation`)**
```
Input: Research findings and notes
Process:
- Advanced synthesis of all research findings
- Professional markdown formatting with clear structure
- Intelligent citation management and source tracking
- Token limit handling with content compression
- Quality-focused final report assembly
Output: Publication-ready research report
```

## 📊 Implementation Comparison

| Feature | Modern (deep_researcher) | Graph Workflow | Multi-Agent Workflow |
|---------|-------------------------|---------------|---------------------|
| **Architecture** | 4-stage pipeline with supervisor | Sequential steps | Supervisor + Researchers |
| **Clarification** | Intelligent scope assessment | Basic user input | Message-based input |
| **Research Planning** | Detailed brief generation | Interactive planning | Direct topic assignment |
| **Execution** | Concurrent research units (3x) | Step-by-step | Parallel execution |
| **Quality Control** | Multi-stage refinement | Multi-iteration sections | Built-in coordination |
| **Web Search** | Native (OpenAI/Anthropic) + APIs | Standard APIs | Standard APIs |
| **Tool Integration** | MCP + Advanced features | Standard search APIs | MCP + Search APIs |
| **Report Quality** | ✅ Advanced synthesis | ✅ Multi-iteration | ✅ Supervisor coordination |
| **Production Ready** | ✅ Fully optimized | ⚠️ Needs supervision | ✅ Automatic |
| **Best Use Case** | **Sophisticated production research** | High-stakes manual oversight | Quick comprehensive analysis |

## 🔧 API Usage Examples

### **Modern Implementation (Recommended)**

```javascript
const response = await fetch('http://localhost:8000/invoke', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    input: {
      messages: [
        { role: "user", content: "Comprehensive analysis of Model Context Protocol implementation strategies" }
      ]
    },
    config: {
      configurable: {
        thread_id: "research_session_001",
        search_api: "tavily",
        research_model: "openai:gpt-4",
        final_report_model: "openai:gpt-4",
        compression_model: "openai:gpt-4-mini",
        max_concurrent_research_units: 3,
        max_researcher_iterations: 3,
        allow_clarification: false,
        max_react_tool_calls: 5
      }
    },
    implementation: "modern"
  })
});

const result = await response.json();
// result.output.final_report contains the comprehensive research report
console.log(result.output.final_report);
```

**Expected Response Structure:**
```json
{
  "output": {
    "final_report": "# Comprehensive Analysis of Model Context Protocol...",
    "messages": [...],
    "research_brief": "Detailed analysis of MCP implementation strategies...",
    "notes": ["Compressed research findings..."]
  },
  "status": "success",
  "implementation": "modern",
  "thread_id": "research_session_001"
}
```

### **Graph Implementation**
```javascript
const response = await fetch('http://localhost:8000/invoke', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    input: {
      topic: "Model Context Protocol implementation strategies"
    },
    config: {
      configurable: {
        search_api: "tavily",
        planner_model: "gpt-4",
        writer_model: "gpt-4",
        auto_approve: true
      }
    },
    implementation: "graph"
  })
});
```

### **Multi-Agent Implementation**
```javascript
const response = await fetch('http://localhost:8000/invoke', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    input: {
      messages: [
        { role: "user", content: "Model Context Protocol implementation strategies" }
      ]
    },
    config: {
      configurable: {
        search_api: "tavily",
        supervisor_model: "gpt-4",
        researcher_model: "gpt-4"
      }
    },
    implementation: "multi_agent"
  })
});
```

## 🌐 Deployment Options

### **Local Development**
```bash
python server.py
# Server runs on http://localhost:8000
# Defaults to modern implementation
```

### **Docker Deployment**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements-server.txt .
RUN pip install -r requirements-server.txt
COPY . .
CMD ["python", "server.py"]
```

### **Cloud Deployment (Vercel/Railway/etc.)**
1. Deploy the LangGraph server to your cloud platform
2. Update `LANGGRAPH_API_URL` to your deployed endpoint
3. Deploy the Next.js frontend with the updated environment variable

## 🎯 Features Enabled

### **Modern Implementation (deep_researcher):** ⭐
- ✅ **4-stage research pipeline** with intelligent coordination
- ✅ **Concurrent processing** with up to 3 research units
- ✅ **Advanced synthesis** with compression and summarization
- ✅ **Intelligent clarification** (auto-bypassed for web)
- ✅ **Professional report generation** with citations
- ✅ **Native web search** (OpenAI/Anthropic integrated)
- ✅ **MCP tool integration** for external APIs
- ✅ **Production optimization** for real-world deployment
- ✅ **Token limit handling** with intelligent content management

### **For Graph Workflow:**
- ✅ **Auto-approval** mode for web interface
- ✅ **Quality evaluation** with iterative improvement
- ✅ **Structured planning** with section organization
- ✅ **Citation management** with source tracking
- ✅ **Multi-model support** (OpenAI, Anthropic, Groq)

### **For Multi-Agent Workflow:**
- ✅ **Parallel processing** for speed
- ✅ **Supervisor coordination** of research team
- ✅ **MCP tool integration** for external APIs
- ✅ **Automatic completion** without user intervention
- ✅ **Configurable research depth** and query count

### **For All Implementations:**
- ✅ **Multiple search APIs**: Tavily, OpenAI, Anthropic, DuckDuckGo
- ✅ **Professional report generation** with markdown formatting
- ✅ **Hebrew language support** for international users
- ✅ **Thread management** for conversation continuity
- ✅ **Error handling** with detailed debugging information

## 🔍 Monitoring and Debugging

### **Health Check Endpoint**
```bash
curl http://localhost:8000/health
```

Returns implementation status and configuration.

### **Available Models Endpoint**
```bash
curl http://localhost:8000/config/models
```

Shows supported providers and configurations for all implementations.

### **Implementation Features Endpoint**
```bash
curl http://localhost:8000/implementations
```

Details about each workflow implementation and their capabilities.

## 🛠️ Troubleshooting

### **Common Issues:**

1. **"Modern implementation missing files"**
   - Ensure complete directory structure:
     ```
     backend_temp/src/open_deep_research/
     ├── deep_researcher.py     # Main workflow
     ├── configuration.py       # Config classes  
     ├── state.py              # State definitions
     ├── utils.py              # Utility functions
     └── prompts.py            # Prompt templates
     ```

2. **"Graph not initialized"**
   - Verify all required dependencies are installed
   - Check environment variables are set
   - Review server startup logs for errors

3. **"Connection refused"**
   - Ensure server is running on expected port
   - Check firewall settings
   - Verify `LANGGRAPH_API_URL` points to correct endpoint

4. **"API key errors"**
   - Verify all required API keys are set in environment
   - Check API key validity and quotas
   - Ensure keys have appropriate permissions

5. **"Token limit exceeded"**
   - Modern implementation handles this automatically
   - Check `compression_model` configuration
   - Verify model token limits in utils.py

### **Debug Mode:**
Start server with verbose logging:
```bash
python server.py --log-level debug
```

## 📈 Performance Optimization

### **For Speed (Recommended: Modern Implementation):**
- Use **modern implementation** with concurrent research units
- Set higher `max_concurrent_research_units` (3-5)
- Use **native web search** (OpenAI/Anthropic)
- Enable **advanced compression** for faster processing
- Configure faster models for compression tasks

### **For Quality (Alternative: Graph Implementation):**
- Use **graph implementation** with quality evaluation
- Set higher `max_search_depth` for thorough research
- Use **Claude models** for better reasoning
- Enable **Tavily search** for higher quality sources

### **For Balance (Alternative: Multi-Agent):**
- Use **multi-agent implementation** for parallel speed
- Configure multiple researchers with good models
- Use **Tavily search** with reasonable query limits

## 🎉 Success!

Your LangGraph research workflows are now:
- 🌐 **Accessible online** through the web interface
- 🚀 **Deployable to cloud** platforms  
- 📱 **Mobile-friendly** with responsive UI
- 🔄 **Scalable** with proper thread management
- 📊 **Monitored** with health checks and debugging
- ⭐ **Production-ready** with modern implementation

Users can now access your sophisticated AI research capabilities through a beautiful, modern web interface while preserving all the power and flexibility of your LangGraph workflows!

## 💡 Implementation Recommendations

- **Start with Modern**: Best overall performance and sophisticated pipeline
- **Use Graph for Critical Research**: When human oversight is needed
- **Use Multi-Agent for Speed**: When fast results are prioritized
- **Configure API Keys**: OpenAI + Anthropic for best model variety
- **Enable MCP Tools**: For advanced external integrations
- **Monitor Performance**: Use health endpoints for system status
- **Optimize for Use Case**: Adjust concurrent units and iterations based on needs 
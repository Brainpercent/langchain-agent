# 🤖 AI Research Assistant Frontend

A modern, responsive frontend for the Open Deep Research agent built with Next.js 14, TypeScript, and Tailwind CSS.

## ✨ Features

- **🔐 Supabase Authentication** - Secure login/signup with JWT tokens
- **💬 Real-time Chat Interface** - Beautiful chat UI with streaming responses
- **📱 Responsive Design** - Works perfectly on desktop and mobile
- **🎨 Modern UI/UX** - Clean, professional interface with Tailwind CSS
- **⚡ Fast Performance** - Next.js 14 with Turbopack for lightning-fast development
- **🔒 Protected Routes** - Authentication required for chat access
- **🌐 API Integration** - Connected to LangGraph backend with Bearer token auth

## 🚀 Quick Start

### Option 1: PowerShell Script (Recommended)
```powershell
.\start-dev.ps1
```

### Option 2: Manual Environment Setup
```powershell
# Set environment variables
$env:NEXT_PUBLIC_SUPABASE_URL = "https://pmschnwcszmwaljxzmgr.supabase.co"
$env:NEXT_PUBLIC_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtc2Nobndjc3ptd2Fsanh6bWdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI5MzU2MjcsImV4cCI6MjA2ODUxMTYyN30.TSiHXFqZf6wd2ruyk8XmyQgh_O2l0Ihp9bU0zUP-_8E"
$env:NEXT_PUBLIC_LANGGRAPH_API_URL = "http://localhost:2024"
$env:NEXT_PUBLIC_ASSISTANT_ID = "e9a5370f-7a53-55a8-ada8-6ab9ef15bb5b"

# Start development server
npm run dev
```

## 🎯 Usage

1. **Start the LangGraph Backend** (in the main project directory):
   ```bash
   uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
   ```

2. **Start the Frontend** (in the frontend directory):
   ```powershell
   .\start-dev.ps1
   ```

3. **Open Your Browser**:
   - Visit: `http://localhost:3000`
   - You'll see the login form first

4. **Create an Account or Sign In**:
   - Use any email/password to create an account
   - Or sign in with existing credentials

5. **Start Chatting**:
   - Ask research questions like:
     - "What are the latest developments in AI research?"
     - "Explain quantum computing in simple terms"
     - "Research the impact of climate change on agriculture"

## 🏗️ Architecture

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout with AuthProvider
│   │   └── page.tsx           # Main page (ChatContainer)
│   ├── components/
│   │   ├── auth/              # Authentication components
│   │   │   ├── AuthProvider.tsx
│   │   │   └── LoginForm.tsx
│   │   └── ui/                # Chat UI components
│   │       ├── ChatContainer.tsx
│   │       ├── ChatInput.tsx
│   │       ├── Message.tsx
│   │       └── MessageList.tsx
│   ├── lib/
│   │   ├── api.ts             # LangGraph API client
│   │   ├── auth.ts            # Supabase authentication
│   │   └── utils.ts           # Utility functions
│   └── types/
│       └── chat.ts            # TypeScript type definitions
```

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key | `eyJhbGciOiJIUzI1NiI...` |
| `NEXT_PUBLIC_LANGGRAPH_API_URL` | LangGraph server URL | `http://localhost:2024` |
| `NEXT_PUBLIC_ASSISTANT_ID` | Assistant ID from LangGraph | `e9a5370f-7a53-55a8...` |

## 🐛 Troubleshooting

### Authentication Issues
- **403 Forbidden**: Make sure LangGraph backend is running and environment variables are set
- **Invalid Credentials**: Verify Supabase URL and API key are correct
- **Session Expired**: Sign out and sign in again

### Connection Issues
- **Backend Not Found**: Ensure LangGraph server is running on port 2024
- **CORS Errors**: Check that the frontend is running on localhost:3000

### Development Issues
- **Module Not Found**: Run `npm install` to ensure all dependencies are installed
- **Build Errors**: Check TypeScript errors in the terminal

## 📦 Dependencies

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety and better development experience
- **Tailwind CSS** - Utility-first CSS framework
- **@supabase/supabase-js** - Supabase client for authentication
- **@headlessui/react** - Unstyled, accessible UI components
- **@heroicons/react** - Beautiful SVG icons
- **react-markdown** - Markdown rendering for AI responses

## 🎨 UI Components

- **ChatContainer** - Main chat interface with authentication guard
- **MessageList** - Scrollable list of messages with auto-scroll
- **Message** - Individual message component with user/assistant styling
- **ChatInput** - Auto-expanding textarea with send button
- **LoginForm** - Authentication form with sign in/up toggle
- **AuthProvider** - Context provider for authentication state

## 🚀 What's Next?

This frontend provides a solid foundation for your AI Research Assistant. Future enhancements could include:

- **Chat History** - Save and load previous conversations
- **Settings Panel** - Configure research parameters
- **File Upload** - Upload documents for research
- **Export Options** - Download research reports
- **Multiple Assistants** - Switch between different AI models

---

**Built with ❤️ using Next.js 14, TypeScript, and Tailwind CSS** 
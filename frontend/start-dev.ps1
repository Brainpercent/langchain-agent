# AI Research Assistant - Development Server Starter
# This script sets the required environment variables and starts the Next.js development server

Write-Host "🚀 Starting AI Research Assistant Frontend..." -ForegroundColor Green
Write-Host "Setting environment variables..." -ForegroundColor Yellow

# Set Supabase environment variables
$env:NEXT_PUBLIC_SUPABASE_URL = "https://pmschnwcszmwaljxzmgr.supabase.co"
$env:NEXT_PUBLIC_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtc2Nobndjc3ptd2Fsanh6bWdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI5MzU2MjcsImV4cCI6MjA2ODUxMTYyN30.TSiHXFqZf6wd2ruyk8XmyQgh_O2l0Ihp9bU0zUP-_8E"

# Set LangGraph API environment variables
$env:NEXT_PUBLIC_LANGGRAPH_API_URL = "http://localhost:2024"
$env:NEXT_PUBLIC_ASSISTANT_ID = "e9a5370f-7a53-55a8-ada8-6ab9ef15bb5b"

Write-Host "Environment variables set successfully!" -ForegroundColor Green
Write-Host "Starting Next.js development server..." -ForegroundColor Yellow

# Start the development server
npm run dev 
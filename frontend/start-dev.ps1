# Load environment variables for local development
Write-Host "🚀 Starting AI Research Assistant Frontend..." -ForegroundColor Green

# Check if we want to use Vercel API (for online deployment testing) or local LangGraph
$useVercelAPI = $env:USE_VERCEL_API
if (-not $useVercelAPI) {
    Write-Host "🤔 Choose your development mode:" -ForegroundColor Yellow
    Write-Host "   [1] Local Development (requires LangGraph server)" -ForegroundColor Cyan
    Write-Host "   [2] Vercel API (for testing online deployment)" -ForegroundColor Cyan
    $choice = Read-Host "Enter choice (1 or 2)"
    
    if ($choice -eq "2") {
        $useVercelAPI = "true"
    } else {
        $useVercelAPI = "false"
    }
}

# Supabase Configuration
$env:NEXT_PUBLIC_SUPABASE_URL = "https://pmschnwcszmwaljxzmgr.supabase.co"
$env:NEXT_PUBLIC_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtc2Nobndjc3ptd2Fsanh6bWdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI5MzU2MjcsImV4cCI6MjA2ODUxMTYyN30.TSiHXFqZf6wd2ruyk8XmyQgh_O2l0Ihp9bU0zUP-_8E"

if ($useVercelAPI -eq "true") {
    # Vercel API Configuration - Uses deployed Vercel endpoints
    $env:NEXT_PUBLIC_API_MODE = "vercel"
    $env:NEXT_PUBLIC_VERCEL_URL = "your-vercel-deployment-url.vercel.app"  # Update this with your actual Vercel URL
    Write-Host "✅ Using Vercel API mode" -ForegroundColor Green
    Write-Host "   - API calls will go through Vercel serverless functions" -ForegroundColor Cyan
    Write-Host "   - Update NEXT_PUBLIC_VERCEL_URL with your actual deployment URL" -ForegroundColor Yellow
} else {
    # Local LangGraph Configuration
    $env:NEXT_PUBLIC_API_MODE = "local"
    $env:NEXT_PUBLIC_LANGGRAPH_API_URL = "http://localhost:2024"
    Write-Host "✅ Using Local LangGraph mode" -ForegroundColor Green
    Write-Host "   - Make sure your LangGraph server is running at localhost:2024" -ForegroundColor Yellow
}

$env:NEXT_PUBLIC_ASSISTANT_ID = "deep_researcher"

Write-Host ""
Write-Host "✅ Environment variables set:" -ForegroundColor Yellow
Write-Host "   - Supabase URL: $env:NEXT_PUBLIC_SUPABASE_URL" -ForegroundColor Cyan
Write-Host "   - API Mode: $env:NEXT_PUBLIC_API_MODE" -ForegroundColor Cyan
Write-Host "   - Assistant ID: $env:NEXT_PUBLIC_ASSISTANT_ID" -ForegroundColor Cyan

if ($useVercelAPI -eq "true") {
    Write-Host "   - Vercel URL: $env:NEXT_PUBLIC_VERCEL_URL" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🌐 Starting development server in Vercel API mode..." -ForegroundColor Green
    Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Yellow
    Write-Host "   API: Uses Vercel serverless functions" -ForegroundColor Yellow
} else {
    Write-Host "   - LangGraph API URL: $env:NEXT_PUBLIC_LANGGRAPH_API_URL" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Make sure your LangGraph server is running!" -ForegroundColor Red
    Write-Host "   To start the LangGraph server, run in the project root:" -ForegroundColor Yellow
    Write-Host "   langgraph dev --allow-blocking" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🌐 Starting development server in Local mode..." -ForegroundColor Green
    Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Yellow
    Write-Host "   LangGraph: http://localhost:2024" -ForegroundColor Yellow
}

Write-Host ""

# Start the development server
npm run dev 
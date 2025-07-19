# AI Research Assistant - Development Server Starter
# This script loads environment variables from .env file and starts the Next.js development server

Write-Host "🚀 Starting AI Research Assistant Frontend..." -ForegroundColor Green
Write-Host "Loading environment variables from .env file..." -ForegroundColor Yellow

# Check if .env file exists
if (Test-Path "../.env") {
    Write-Host "Found .env file - loading environment variables..." -ForegroundColor Green
    
    # Load .env file
    Get-Content "../.env" | ForEach-Object {
        if ($_ -match "^([^#].*)=(.*)$") {
            $name = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
            Write-Host "Set $name" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Red
    Write-Host "Please create a .env file with your credentials." -ForegroundColor Yellow
    Write-Host "Required variables:" -ForegroundColor Yellow
    Write-Host "  NEXT_PUBLIC_SUPABASE_URL=your_supabase_url" -ForegroundColor Gray
    Write-Host "  NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_key" -ForegroundColor Gray
    Write-Host "  NEXT_PUBLIC_LANGGRAPH_API_URL=http://localhost:2024" -ForegroundColor Gray
    Write-Host "  NEXT_PUBLIC_ASSISTANT_ID=Deep Researcher" -ForegroundColor Gray
    exit 1
}

Write-Host "Environment variables loaded successfully!" -ForegroundColor Green
Write-Host "Starting Next.js development server..." -ForegroundColor Yellow

# Start the development server
npm run dev 
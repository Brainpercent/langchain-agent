# AI Research Assistant - Development Server Starter
# This script loads environment variables from .env file and starts the Next.js development server

Write-Host "🚀 Starting AI Research Assistant Frontend..." -ForegroundColor Green
Write-Host "Setting up environment variables..." -ForegroundColor Yellow

# Set the correct frontend environment variables for Vercel deployment
[Environment]::SetEnvironmentVariable("NEXT_PUBLIC_SUPABASE_URL", "https://pmschnwcszmwaljxzmgr.supabase.co", "Process")
[Environment]::SetEnvironmentVariable("NEXT_PUBLIC_SUPABASE_ANON_KEY", "sb_publishable_2UpeYuhWRq7wLqYlsl3p3Q_nS3g-2Wh", "Process")
[Environment]::SetEnvironmentVariable("NEXT_PUBLIC_LANGGRAPH_API_URL", "https://langchain-agent-kv9qu5rik-edwards-projects-f73afe36.vercel.app/api", "Process")
[Environment]::SetEnvironmentVariable("NEXT_PUBLIC_ASSISTANT_ID", "Deep Researcher", "Process")

Write-Host "✅ Set NEXT_PUBLIC_SUPABASE_URL" -ForegroundColor Green
Write-Host "✅ Set NEXT_PUBLIC_SUPABASE_ANON_KEY" -ForegroundColor Green  
Write-Host "✅ Set NEXT_PUBLIC_LANGGRAPH_API_URL (Vercel deployment)" -ForegroundColor Green
Write-Host "✅ Set NEXT_PUBLIC_ASSISTANT_ID" -ForegroundColor Green

# Check if .env file exists for additional backend variables
if (Test-Path "../.env") {
    Write-Host "Found .env file - loading backend environment variables..." -ForegroundColor Yellow
    
    # Load .env file for backend variables only
    Get-Content "../.env" | ForEach-Object {
        if ($_ -match "^([^#].*)=(.*)$") {
            $name = $matches[1]
            $value = $matches[2]
            # Only load non-frontend variables
            if (-not $name.StartsWith("NEXT_PUBLIC_")) {
                [Environment]::SetEnvironmentVariable($name, $value, "Process")
                Write-Host "Set $name" -ForegroundColor Gray
            }
        }
    }
} else {
    Write-Host "⚠️  Note: .env file not found (optional for frontend)" -ForegroundColor Yellow
}

Write-Host "Environment variables configured successfully!" -ForegroundColor Green
Write-Host "Starting Next.js development server..." -ForegroundColor Yellow

# Start the development server
npm run dev 
#!/usr/bin/env node

console.log('=== Server Startup Debug ===')
console.log('Node version:', process.version)
console.log('Platform:', process.platform)
console.log('Architecture:', process.arch)
console.log('Current working directory:', process.cwd())

// Check if the standalone server exists
const fs = require('fs')
const path = require('path')

const serverPath = path.join(process.cwd(), 'frontend/.next/standalone/server.js')
console.log('Server path:', serverPath)
console.log('Server exists:', fs.existsSync(serverPath))

if (!fs.existsSync(serverPath)) {
  console.error('❌ Standalone server not found!')
  console.log('Looking for .next directory...')
  const nextPath = path.join(process.cwd(), 'frontend/.next')
  console.log('.next exists:', fs.existsSync(nextPath))
  
  if (fs.existsSync(nextPath)) {
    console.log('Contents of .next:', fs.readdirSync(nextPath))
  }
  process.exit(1)
}

// Set environment variables for Railway
const PORT = process.env.PORT || '8080'
const HOSTNAME = process.env.HOSTNAME || '0.0.0.0'

console.log(`Setting up server on ${HOSTNAME}:${PORT}`)

// Ensure environment variables are set
process.env.PORT = PORT
process.env.HOSTNAME = HOSTNAME

console.log('Environment variables set:')
console.log('PORT:', process.env.PORT)
console.log('HOSTNAME:', process.env.HOSTNAME)

console.log('Starting Next.js server...')

try {
  // Start the Next.js standalone server
  require(serverPath)
  console.log('✅ Server started successfully')
} catch (error) {
  console.error('❌ Error starting server:', error)
  process.exit(1)
} 
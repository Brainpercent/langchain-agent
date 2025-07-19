#!/usr/bin/env node

// Ensure environment variables are set for Railway
process.env.PORT = process.env.PORT || '8080'
process.env.HOSTNAME = process.env.HOSTNAME || '0.0.0.0'

console.log(`Starting server on ${process.env.HOSTNAME}:${process.env.PORT}`)

// Start the Next.js standalone server
require('./frontend/.next/standalone/server.js') 
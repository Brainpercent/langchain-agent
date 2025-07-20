#!/usr/bin/env node

/**
 * Vercel Deployment Script for LangGraph Deep Research
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Preparing LangGraph Deep Research for Vercel deployment...\n');

// Check if required files exist
const requiredFiles = [
  'backend_temp/src/open_deep_research/deep_researcher.py',
  'backend_temp/src/open_deep_research/configuration.py',
  'backend_temp/src/open_deep_research/state.py',
  'backend_temp/src/open_deep_research/utils.py',
  'backend_temp/src/open_deep_research/prompts.py',
  'api/langgraph.py',
  'vercel.json',
  'requirements-vercel.txt'
];

console.log('📋 Checking required files...');
const missingFiles = [];
for (const file of requiredFiles) {
  if (!fs.existsSync(file)) {
    missingFiles.push(file);
  } else {
    console.log(`✅ ${file}`);
  }
}

if (missingFiles.length > 0) {
  console.log('\n❌ Missing required files:');
  missingFiles.forEach(file => console.log(`   - ${file}`));
  console.log('\nPlease ensure all LangGraph implementation files are in place.');
  process.exit(1);
}

// Check environment variables
console.log('\n🔑 Checking environment variables...');
const requiredEnvVars = ['OPENAI_API_KEY', 'TAVILY_API_KEY'];
const missingEnvVars = [];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    missingEnvVars.push(envVar);
  } else {
    console.log(`✅ ${envVar} configured`);
  }
}

if (missingEnvVars.length > 0) {
  console.log('\n⚠️ Missing environment variables:');
  missingEnvVars.forEach(envVar => console.log(`   - ${envVar}`));
  console.log('\nThese will need to be configured in Vercel dashboard.');
}

// Check Vercel CLI
console.log('\n🔧 Checking Vercel CLI...');
try {
  execSync('vercel --version', { stdio: 'pipe' });
  console.log('✅ Vercel CLI installed');
} catch (error) {
  console.log('❌ Vercel CLI not found');
  console.log('Install with: npm install -g vercel');
  process.exit(1);
}

// Build check
console.log('\n📦 Running build check...');
try {
  execSync('npm run build', { stdio: 'inherit' });
  console.log('✅ Build successful');
} catch (error) {
  console.log('❌ Build failed');
  console.log('Please fix build errors before deploying.');
  process.exit(1);
}

console.log('\n🎯 Ready for deployment!\n');

console.log('📋 Deployment Steps:');
console.log('1. Run: vercel');
console.log('2. Follow the prompts to link your project');
console.log('3. Set environment variables in Vercel dashboard:');
console.log('   - OPENAI_API_KEY');
console.log('   - TAVILY_API_KEY');
console.log('   - ANTHROPIC_API_KEY (optional)');
console.log('4. Deploy: vercel --prod');

console.log('\n🌟 Features enabled:');
console.log('✅ LangGraph Deep Research integration');
console.log('✅ Modern implementation with 4-stage pipeline');
console.log('✅ Vercel-optimized configuration');
console.log('✅ OpenAI fallback for reliability');
console.log('✅ Auto-scaling serverless functions');

console.log('\n🚀 Deploy now? Run: vercel --prod'); 
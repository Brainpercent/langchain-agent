/** @type {import('next').NextConfig} */
const path = require('path')

const nextConfig = {
  // Enable standalone output for Docker
  output: 'standalone',
  
  // Environment variables that should be available at build time
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXT_PUBLIC_LANGGRAPH_API_URL: process.env.NEXT_PUBLIC_LANGGRAPH_API_URL,
    NEXT_PUBLIC_ASSISTANT_ID: process.env.NEXT_PUBLIC_ASSISTANT_ID,
  },

  // Image optimization for better performance
  images: {
    domains: ['localhost'],
    unoptimized: true, // Better for containerized environments
  },

  // Webpack configuration for better bundling and path resolution
  webpack: (config, { isServer }) => {
    // Add path aliases
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, 'src'),
      '@/components': path.resolve(__dirname, 'src/components'),
      '@/lib': path.resolve(__dirname, 'src/lib'),
      '@/types': path.resolve(__dirname, 'src/types'),
    }

    // Optimize for production builds
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      }
    }
    return config
  },
}

module.exports = nextConfig 
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  eslint: {
    // Disable ESLint during build
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Disable TypeScript checks during build if needed
    ignoreBuildErrors: false,
  },
  env: {
    // Provide fallback values for build time
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost:54321',
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-key',
    NEXT_PUBLIC_LANGGRAPH_API_URL: process.env.NEXT_PUBLIC_LANGGRAPH_API_URL || 'http://localhost:2024',
    NEXT_PUBLIC_ASSISTANT_ID: process.env.NEXT_PUBLIC_ASSISTANT_ID || 'default',
  },
  images: {
    unoptimized: true
  }
};

module.exports = nextConfig; 
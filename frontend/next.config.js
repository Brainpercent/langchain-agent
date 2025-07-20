/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    // Disable ESLint during build
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Disable TypeScript checks during build if needed
    ignoreBuildErrors: false,
  },
  images: {
    unoptimized: true
  }
};

module.exports = nextConfig; 
/** @type {import('next').NextConfig} */
const path = require('path');

const nextConfig = {
  output: 'standalone',
  outputFileTracingRoot: process.env.NODE_ENV === 'production' ? '/app' : undefined,
  
  // Webpack configuration for path resolution
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Ensure proper path resolution for Railway deployment
    const srcPath = path.resolve(__dirname, 'src');
    
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': srcPath,
      '@/components': path.resolve(srcPath, 'components'),
      '@/lib': path.resolve(srcPath, 'lib'),
      '@/types': path.resolve(srcPath, 'types'),
    };
    
    // Ensure module resolution includes src directory
    config.resolve.modules = [
      path.resolve(__dirname, 'src'),
      'node_modules',
      ...(config.resolve.modules || [])
    ];
    
    return config;
  },
  
  // Image optimization
  images: {
    unoptimized: true // Better for containerized environments
  }
};

module.exports = nextConfig; 
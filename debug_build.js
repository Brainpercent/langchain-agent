const fs = require('fs');
const path = require('path');

console.log('=== Build Environment Debug ===');
console.log('Current working directory:', process.cwd());
console.log('__dirname:', __dirname);

// Check if we're in the right directory
const frontendPath = path.join(__dirname, 'frontend');
const srcPath = path.join(frontendPath, 'src');
const libPath = path.join(srcPath, 'lib');

console.log('Frontend path exists:', fs.existsSync(frontendPath));
console.log('Src path exists:', fs.existsSync(srcPath));
console.log('Lib path exists:', fs.existsSync(libPath));

if (fs.existsSync(libPath)) {
  console.log('Files in lib:', fs.readdirSync(libPath));
}

if (fs.existsSync(srcPath)) {
  console.log('Directories in src:', fs.readdirSync(srcPath));
}

// Try relative imports from components
const componentsPath = path.join(srcPath, 'components', 'auth');
if (fs.existsSync(componentsPath)) {
  console.log('Auth components path exists');
  const relativePath = path.relative(componentsPath, libPath);
  console.log('Relative path from auth to lib:', relativePath);
} 
const fs = require('fs');
const path = require('path');

function listDirectory(dirPath, indent = '') {
  try {
    const items = fs.readdirSync(dirPath);
    console.log(`${indent}${path.basename(dirPath)}/`);
    items.forEach(item => {
      const itemPath = path.join(dirPath, item);
      const stat = fs.statSync(itemPath);
      if (stat.isDirectory()) {
        listDirectory(itemPath, indent + '  ');
      } else {
        console.log(`${indent}  ${item}`);
      }
    });
  } catch (err) {
    console.log(`${indent}ERROR: Cannot read ${dirPath} - ${err.message}`);
  }
}

console.log('=== Build Environment Debug ===');
console.log('Current working directory:', process.cwd());
console.log('__dirname:', __dirname);

// List all contents
console.log('\n=== Full Directory Structure ===');
listDirectory(__dirname);

// Check specific paths
const frontendPath = path.join(__dirname, 'frontend');
const srcPath = path.join(frontendPath, 'src');
const libPath = path.join(srcPath, 'lib');

console.log('\n=== Path Checks ===');
console.log('Frontend path exists:', fs.existsSync(frontendPath));
console.log('Src path exists:', fs.existsSync(srcPath));
console.log('Lib path exists:', fs.existsSync(libPath));

if (fs.existsSync(libPath)) {
  console.log('Files in lib:', fs.readdirSync(libPath));
} else {
  console.log('❌ LIB DIRECTORY IS MISSING!');
  
  // Try to find lib directory elsewhere
  const possiblePaths = [
    path.join(__dirname, 'lib'),
    path.join(__dirname, 'src', 'lib'),
    path.join(frontendPath, 'lib')
  ];
  
  console.log('\n=== Searching for lib directory ===');
  possiblePaths.forEach(p => {
    console.log(`Checking ${p}: ${fs.existsSync(p)}`);
  });
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
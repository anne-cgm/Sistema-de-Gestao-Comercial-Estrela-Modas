const fs = require('fs');
const path = require('path');

const requiredFiles = ['index.html', 'script.js'];

for (const file of requiredFiles) {
  const fullPath = path.join(__dirname, file);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Arquivo obrigatório ausente: ${file}`);
  }
}

console.log('Build OK: arquivos principais do projeto encontrados.');

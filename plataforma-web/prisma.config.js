// prisma.config.js
const { execSync } = require('child_process');

// Carrega as variáveis do arquivo .env nativamente no Node
try {
  require('fs').readFileSync('.env', 'utf8')
    .split('\n')
    .forEach(line => {
      const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
      if (match) {
        const key = match[1];
        let value = match[2] || '';
        if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
        process.env[key] = value;
      }
    });
} catch (e) {
  // Se não encontrar o .env, segue em frente
}

module.exports = {
  datasource: {
    url: process.env.DATABASE_URL,
  },
};
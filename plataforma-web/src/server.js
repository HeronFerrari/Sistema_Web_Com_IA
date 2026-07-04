// src/server.js
require('dotenv').config();

const express = require('express');
const path = require('path');
const routes = require('./routes');

const app = express();

// Middleware para o Express entender JSON nativamente
app.use(express.json());

// Serve o Front-end (HTML/CSS/JS) da pasta public/ — sem CORS, mesma origem
app.use(express.static(path.join(__dirname, '..', 'public')));

// Injeta as rotas da API no servidor
app.use(routes);

const PORTA = 3000;
app.listen(PORTA, () => {
  console.log(`🚀 Servidor Web do PROAGRO Smart rodando em http://localhost:${PORTA}`);
  console.log(`🎨 Front-end disponível em: http://localhost:${PORTA}/`);
});
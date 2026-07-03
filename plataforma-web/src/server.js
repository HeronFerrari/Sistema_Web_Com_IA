// src/server.js
require('dotenv').config();

const express = require('express');
const routes = require('./routes');

const app = express();

// Middleware para o Express entender JSON nativamente
app.use(express.json());

// Injeta as rotas no servidor
app.use(routes);

const PORTA = 3000;
app.listen(PORTA, () => {
  console.log(`🚀 Servidor Web do PROAGRO Smart rodando em http://localhost:${PORTA}`);
});
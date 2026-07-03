// src/routes.js
const { Router } = require('express');
const PropostaController = require('./controllers/PropostaController');

const routes = Router();

// Rota principal onde o front-end vai enviar as propostas de crédito
routes.post('/propostas', PropostaController.criar);

module.exports = routes;
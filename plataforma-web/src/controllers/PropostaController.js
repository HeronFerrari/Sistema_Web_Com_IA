// src/controllers/PropostaController.js
const AnaliseCreditoService = require('../services/AnaliseCreditoService');

class PropostaController {
  async criar(req, res) {
    try {
      // O front-end envia os dados no corpo (body) da requisição
      const dadosProposta = req.body;
      
      // Executa o fluxo de gravação + análise da IA
      const propostaProcessada = await AnaliseCreditoService.processarProposta(dadosProposta);
      
      // Retorna para o front-end a proposta salva com o veredito final
      return res.status(201).json(propostaProcessada);
    } catch (error) {
      return res.status(400).json({ erro: error.message });
    }
  }
}

module.exports = new PropostaController();
// src/services/AnaliseCreditoService.js
const { PrismaClient } = require('@prisma/client');
const axios = require('axios');


const prisma = new PrismaClient();

const IA_API_URL = 'http://127.0.0.1:8000/analisar-proposta';

class AnaliseCreditoService {
  async processarProposta(dados) {
    // 1. Criar ou buscar o Produtor no PostgreSQL
    const produtor = await prisma.produtor.upsert({
      where: { cpf: dados.cpf_produtor },
      update: {
        score_credito: dados.score_credito,
        solicitacoes_recusadas: dados.solicitacoes_recusadas,
        historico_restricoes: dados.historico_restricoes
      },
      create: {
        cpf: dados.cpf_produtor,
        nome: dados.nome_produtor || "Produtor Cadastrado",
        score_credito: dados.score_credito,
        solicitacoes_recusadas: dados.solicitacoes_recusadas,
        historico_restricoes: dados.historico_restricoes
      }
    });

    // 2. Criar ou buscar a Propriedade (CAR) no PostgreSQL
    const propriedade = await prisma.propriedade.upsert({
      where: { car_codigo: dados.car_propriedade },
      update: {
        divergencia_area_car: dados.divergencia_area_car,
        indice_inadimplencia_regiao: dados.indice_inadimplencia_regiao
      },
      create: {
        car_codigo: dados.car_propriedade,
        divergencia_area_car: dados.divergencia_area_car,
        indice_inadimplencia_regiao: dados.indice_inadimplencia_regiao
      }
    });

    // 3. Disparar a requisição para a nossa API de IA em Python
    let resultadoIA;
    try {
      const respostaIA = await axios.post(IA_API_URL, {
        cpf_produtor: dados.cpf_produtor,
        car_propriedade: dados.car_propriedade,
        valor_solicitado: dados.valor_solicitado,
        operacoes_ativas_valor: dados.operacoes_ativas_valor,
        cpf_regular: dados.cpf_regular,
        car_regular: dados.car_regular,
        score_credito: dados.score_credito,
        solicitacoes_recusadas: dados.solicitacoes_recusadas,
        divergencia_area_car: dados.divergencia_area_car,
        historico_restricoes: dados.historico_restricoes,
        indice_inadimplencia_regiao: dados.indice_inadimplencia_regiao
      });
      resultadoIA = respostaIA.data;
    } catch (error) {
      console.error("Erro ao conectar com o motor de IA em Python:", error.message);
      throw new Error("O motor de análise inteligente está temporariamente fora do ar.");
    }

    // 4. Salvar o veredito final da Proposta no PostgreSQL vinculado ao Produtor e Propriedade
    const novaProposta = await prisma.proposta.create({
      data: {
        valor_solicitado: dados.valor_solicitado,
        operacoes_ativas_valor: dados.operacoes_ativas_valor,
        status_analise: resultadoIA.status,
        tecnica_bloqueio: resultadoIA.tecnica_bloqueio,
        justificativas: resultadoIA.justificativas,
        produtor_id: produtor.id,
        propriedade_id: propriedade.id
      }
    });

    return novaProposta;
  }
}

module.exports = new AnaliseCreditoService();
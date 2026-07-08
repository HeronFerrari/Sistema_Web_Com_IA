# backend-ia/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

# Importando os dois módulos que você acabou de codificar!
from sistema_especialista import avaliar_regras_mcr
from analise_grafos import verificar_fracionamento_car

app = FastAPI(title="PROAGRO Smart - Motor Híbrido de IA")

# 1. Carrega o modelo Random Forest que você treinou
caminho_modelo = os.path.join('models', 'modelo_proagro_rf.pkl')
if os.path.exists(caminho_modelo):
    modelo_rf = joblib.load(caminho_modelo)
    print("Modelo Random Forest carregado com sucesso!")
else:
    modelo_rf = None
    print("Aviso: Modelo Random Forest não encontrado. Rode 'treinar_modelo.py' primeiro.")

# 2. Define a estrutura de dados que a API espera receber (Contrato)
class PropostaCredito(BaseModel):
    cpf_produtor: str
    car_propriedade: str
    valor_solicitado: float
    operacoes_ativas_valor: float
    cpf_regular: bool
    car_regular: bool
    score_credito: int
    solicitacoes_recusadas: int
    divergencia_area_car: int
    historico_restricoes: int
    indice_inadimplencia_regiao: float

@app.get("/")
def raiz():
    return {"status": "Online", "projeto": "PROAGRO Smart - API de Sistemas Inteligentes"}

# 3. Rota Principal que une as 3 técnicas de IA
@app.post("/analisar-proposta")
def analisar_proposta(proposta: PropostaCredito):
    print("--- PAYLOAD RECEBIDO NO PYTHON ---")
    print("\n[ATENÇÃO] O PYTHON RECEBEU DIVERGENCIA =", proposta.divergencia_area_car)
    # --- PILAR 1: Sistema Especialista (MCR) ---
    resultado_mcr = avaliar_regras_mcr(
        valor_solicitado=proposta.valor_solicitado,
        operacoes_ativas_valor=proposta.operacoes_ativas_valor,
        cpf_regular=proposta.cpf_regular,
        car_regular=proposta.car_regular,
        divergencia_area_car=proposta.divergencia_area_car
    )
    
    # Se o Sistema Especialista barrar por compliance, já podemos parar aqui
    if resultado_mcr["status"] == "Bloqueado":
        return {
            "status": "Bloqueado",
            "tecnica_bloqueio": "Sistema Especialista (Regras MCR)",
            "justificativas": resultado_mcr["motivos"]
        }
        
    # --- PILAR 2: Grafos de Relacionamento (NetworkX) ---
    resultado_grafo = verificar_fracionamento_car(
        cpf_alvo=proposta.cpf_produtor,
        car_alvo=proposta.car_propriedade
    )
    
    if resultado_grafo["suspeito_fracionamento"]:
        return {
            "status": "Bloqueado",
            "tecnica_bloqueio": "Grafos de Relacionamento (Network Science)",
            "justificativas": [resultado_grafo["detalhes"]]
        }
        
    # --- PILAR 3: Machine Learning (Random Forest) ---
    justificativas_ml = []
    status_final = "Aprovado"
    
    if modelo_rf:
        # Prepara os dados tabulares exatamente no formato que o modelo foi treinado
        dados_entrada = [[
            proposta.score_credito,
            proposta.solicitacoes_recusadas,
            proposta.divergencia_area_car,
            proposta.historico_restricoes,
            proposta.indice_inadimplencia_regiao
        ]]
        
        # Predição: 0 para Normal, 1 para Anômalo/Suspeito
        predicao = modelo_rf.predict(dados_entrada)[0]
        # Probabilidade da predição
        probabilidades = modelo_rf.predict_proba(dados_entrada)[0]
        porcentagem_risco = probabilidades[1] * 100
        
        if predicao == 1:
            status_final = "Bloqueado"
            justificativas_ml.append(f"Machine Learning: Detectado padrão de comportamento de alto risco/anomalia (Confiança: {porcentagem_risco:.2f}%).")
        else:
            justificativas_ml.append(f"Machine Learning: Perfil estatístico considerado seguro (Risco estimado: {porcentagem_risco:.2f}%).")
    else:
        justificativas_ml.append("Machine Learning: Modelo indisponível para análise estatística.")

    # Retorno final caso passe pelas regras e pelo grafo
    return {
        "status": status_final,
        "tecnica_bloqueio": "Machine Learning (Random Forest)" if status_final == "Bloqueado" else "Nenhuma",
        "justificativas": justificativas_ml if status_final == "Bloqueado" else ["Aprovado nos critérios normativos, relacionais e estatísticos."]
    }
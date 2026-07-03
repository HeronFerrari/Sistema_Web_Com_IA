# backend-ia/gerar_dados_sinteticos.py
import pandas as pd
import random
import os

def gerar_dataset_proagro(num_amostras=1000):
    print("Gerando dados sintéticos para o Random Forest...")
    
    dados = []
    
    for _ in range(num_amostras):
        # 1. Variáveis Cadastrais e Financeiras Simuladas
        score_credito = random.randint(300, 1000)               # Score de 300 a 1000
        solicitacoes_recusadas = random.randint(0, 5)            # Quantas vezes já teve crédito negado
        divergencia_area_car = random.choice([0, 0, 0, 0, 1])   # 1 se a área declarada não bate com o satélite (20% de chance)
        historico_restricoes = random.choice([0, 0, 0, 1])      # 1 se já teve restrições cadastrais no passado (25% de chance)
        indice_inadimplencia_regiao = round(random.uniform(0.01, 0.15), 2) # Taxa de calote da região (1% a 15%)
        
        # 2. Lógica de Negócio para Criar a nossa Variável Alvo (Suspeito de Fraude/Anormalidade)
        # Vamos criar regras para que o modelo Random Forest tenha padrões claros para aprender
        pontos_risco = 0
        if score_credito < 500: pontos_risco += 3
        if solicitacoes_recusadas >= 3: pontos_risco += 2
        if divergencia_area_car == 1: pontos_risco += 3
        if historico_restricoes == 1: pontos_risco += 2
        if indice_inadimplencia_regiao > 0.10: pontos_risco += 1
        
        # Se acumular muitos pontos de risco, a proposta é classificada como Anômala/Suspeita (1)
        # Caso contrário, é uma proposta Normal (0)
        anormalidade_detectada = 1 if pontos_risco >= 5 else 0
        
        dados.append({
            "score_credito": score_credito,
            "solicitacoes_recusadas": solicitacoes_recusadas,
            "divergencia_area_car": divergencia_area_car,
            "historico_restricoes": historico_restricoes,
            "indice_inadimplencia_regiao": indice_inadimplencia_regiao,
            "anormalidade_detectada": anormalidade_detectada # Nossa coluna alvo (Label)
        })
        
    # 3. Transforma a lista em uma tabela (DataFrame) do Pandas
    df = pd.DataFrame(dados)
    
    # Garante que a pasta 'data' exista
    os.makedirs('data', exist_ok=True)
    
    # Salva em formato CSV na pasta correta
    caminho_salvamento = os.path.join('data', 'dados_proagro.csv')
    df.to_csv(caminho_salvamento, index=False)
    
    print(f"Sucesso! Arquivo gerado em: {caminho_salvamento}")
    print(df.head()) # Mostra as primeiras 5 linhas da tabela gerada

if __name__ == "__main__":
    gerar_dataset_proagro(1000)
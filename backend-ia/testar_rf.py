import joblib
import os
import pandas as pd

# 1. Carrega o seu modelo treinado
caminho_modelo = os.path.join('models', 'modelo_proagro_rf.pkl')
modelo_rf = joblib.load(caminho_modelo)

def simular_ia(score, recusadas, divergencia, restricoes, inadimplencia_regiao):
    # Organiza os dados na ordem exata do seu CSV
    colunas = [
        'score_credito', 
        'solicitacoes_recusadas', 
        'divergencia_area_car', 
        'historico_restricoes', 
        'indice_inadimplencia_regiao'
    ]
    
    dados_df = pd.DataFrame([[score, recusadas, divergencia, restricoes, inadimplencia_regiao]], columns=colunas)

    # Roda a predição (0 = Seguro, 1 = Alto Risco)
    predicao = modelo_rf.predict(dados_df)[0]
    probabilidades = modelo_rf.predict_proba(dados_df)[0]
    
    status = "Bloqueado (Alto Risco)" if predicao == 1 else "Aprovado (Seguro)"
    confianca = probabilidades[predicao] * 100
    
    print(f"Resultados para Score={score} | Restrições={restricoes}:")
    print(f"  -> Veredito: {status}")
    print(f"  -> Confiança do Modelo: {confianca:.2f}%\n")

# --- CENÁRIOS DE TESTE ---
print("--- TESTANDO VARIÁVEIS DO RANDOM FOREST ---\n")

# Cenário A: Produtor com score moderado e histórico limpo
simular_ia(score=720, recusadas=0, divergencia=0, restricoes=0, inadimplencia_regiao=0.03)

# Cenário B: O cenário que você testou na tela (Score baixo + Restrição)
simular_ia(score=450, recusadas=4, divergencia=0, restricoes=1, inadimplencia_regiao=0.05)

# Cenário C: No limite (Score razoável, mas muitas recusas e restrição ativa)
simular_ia(score=600, recusadas=3, divergencia=0, restricoes=1, inadimplencia_regiao=0.12)
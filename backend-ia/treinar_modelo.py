# backend-ia/treinar_modelo.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def treinar_random_forest():
    print("--- Iniciando o Treinamento do Random Forest ---")
    
    # 1. Carrega o arquivo CSV que geramos no passo anterior
    caminho_csv = os.path.join('data', 'dados_proagro.csv')
    if not os.path.exists(caminho_csv):
        print(f"Erro: O arquivo {caminho_csv} não foi encontrado. Rode o gerador de dados primeiro.")
        return
        
    df = pd.read_csv(caminho_csv)
    
    # 2. Separa o que são Características (X) e o que é o Alvo/Resposta (y)
    X = df.drop(columns=["anormalidade_detectada"]) # Tudo menos a resposta
    y = df["anormalidade_detectada"]                # Apenas a resposta (0 ou 1)
    
    # 3. Divide os dados: 80% para o modelo estudar (treino) e 20% para testar se ele aprendeu (teste)
    X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Inicializa o algoritmo Random Forest
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # 5. Treina o modelo!
    modelo.fit(X_treino, y_treino)
    
    # 6. Avalia a performance do modelo com os 20% de teste que ele nunca viu
    predicoes = modelo.predict(X_teste)
    acuracia = accuracy_score(y_teste, predicoes)
    
    print(f"\nTreinamento Concluído com Sucesso!")
    print(f"Acurácia do Modelo: {acuracia * 100:.2f}%")
    print("\nRelatório de Classificação:")
    print(classification_report(y_teste, predicoes))
    
    # 7. Mostra o "Feature Importance" (O que o modelo achou mais importante para decidir)
    print("\nImportância das Variáveis (Feature Importance):")
    for feature, importancia in zip(X.columns, modelo.feature_importances_):
        print(f"- {feature}: {importancia * 100:.2f}%")
        
    # 8. Salva o modelo treinado na pasta 'models/' para usarmos na API depois
    os.makedirs('models', exist_ok=True)
    caminho_modelo = os.path.join('models', 'modelo_proagro_rf.pkl')
    joblib.dump(modelo, caminho_modelo)
    print(f"\nModelo salvo com sucesso em: {caminho_modelo}")

if __name__ == "__main__":
    treinar_random_forest()
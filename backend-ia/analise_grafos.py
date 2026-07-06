# backend-ia/analise_grafos.py
import networkx as nx

def verificar_fracionamento_car(cpf_alvo, car_alvo):
    """
    Usa NetworkX para varrer conexões entre CPFs e CARs.
    Detecta se múltiplos CPFs conectados por vínculo familiar compartilham o mesmo CAR.
    """
    # 1. Inicializa um Grafo não-direcionado
    G = nx.Graph()
    
    # 2. Simulando nossa Base de Dados Relacional (Dados Sintéticos)
    # Relações de propriedade: Quem é dono de qual CAR
    vinculos_propriedade = [
        ("11111111111", "999999"), #Fazenda A
        ("22222222222", "888888"), #Fazenda B
        ("33333333333", "777777"), #Fazenda C
        ("44444444444", "777777"),  # Fazenda C
    ]
    
    # Relações familiares/sociedades: Quem é parente de quem
    vinculos_familiares = [
        ("33333333333", "44444444444"), # Parentes/Sócios
        ("11111111111", "22222222222")
    ]
    
    # 3. Alimenta o Grafo com os nós e conexões
    for cpf, car in vinculos_propriedade:
        G.add_edge(cpf, car, tipo="propriedade")
        
    for cpf1, cpf2 in vinculos_familiares:
        G.add_edge(cpf1, cpf2, tipo="familia")
        
    # --- ALGORITMO DE IA (Busca de Vizinhança e Caminhos) ---
    # Se o CAR alvo não existe no grafo, ele está livre e seguro
    if not G.has_node(car_alvo):
        return {"suspeito_fracionamento": False, "detalhes": "Nenhum vínculo prévio encontrado para este CAR."}
        
    # Descobre todos os CPFs que já estão vinculados a esse CAR específico
    vizinhos_do_car = [no for no in G.neighbors(car_alvo)]
    
    # Verifica se o CPF que está pedindo o crédito agora tem relação familiar com quem já usa o CAR
    for cpf_vinculado in vizinhos_do_car:
        if cpf_vinculado == cpf_alvo:
            continue # É o próprio produtor olhando seu próprio histórico
            
        # O NetworkX verifica se existe um caminho ("path") de parentesco entre o alvo e quem já usa o CAR
        if nx.has_path(G, cpf_alvo, cpf_vinculado):
            # Encontra o caminho exato para podermos justificar na tela
            caminho = nx.shortest_path(G, cpf_alvo, cpf_vinculado)
            return {
                "suspeito_fracionamento": True,
                "detalhes": f"Alerta de Fracionamento! O CAR '{car_alvo}' já possui operações ativas associadas a '{cpf_vinculado}', que possui vínculo detectado com o solicitante através do caminho: {' -> '.join(caminho)}."
            }
            
    return {
        "suspeito_fracionamento": False,
        "detalhes": "CAR compartilhado, mas sem vínculos familiares diretos detectados entre os produtores."
    }

# --- Cenário de Teste Rápido ---
if __name__ == "__main__":
    print("--- Testando Módulo de Grafos (PROAGRO Smart) ---\n")
    
    # Cenário de Risco: David tenta pedir crédito para a 'CAR_Fazenda_C'
    # Mas a Mariana (sua parente) já está usando esse mesmo CAR!
    solicitante = "CPF_David"
    propriedade = "CAR_Fazenda_C"
    
    resultado = verificar_fracionamento_car(solicitante, propriedade)
    
    print(f"Análise de Risco para {solicitante} no {propriedade}:")
    print(f"Suspeito? {resultado['suspeito_fracionamento']}")
    print(f"Parecer: {resultado['detalhes']}")
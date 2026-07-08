import asyncio
import httpx
import time

API_URL = "http://127.0.0.1:8000/analisar-proposta"

# 1. Definimos os cenários que testam cada pilar do Motor Híbrido
CENARIOS = {
    "especialista": {
        "cpf_produtor": "000.000.000-00",
        "car_propriedade": "BR-PR-0000",
        "valor_solicitado": 200000.00, "operacoes_ativas_valor": 350000.00,  # Estoura limite (MCR)
        "cpf_regular": True, "car_regular": True, "divergencia_area_car": 0,
        "score_credito": 800, "solicitacoes_recusadas": 0, "historico_restricoes": 0, "indice_inadimplencia_regiao": 0.02
    },
    "grafos": {
        # Passe aqui o CPF e CAR que o seu arquivo analise_grafos.py pega como fracionamento
        "cpf_produtor": "333.333.333-33",  
        "car_propriedade": "111111",
        "valor_solicitado": 50000.00, "operacoes_ativas_valor": 0.00,
        "cpf_regular": True, "car_regular": True, "divergencia_area_car": 0,
        "score_credito": 800, "solicitacoes_recusadas": 0, "historico_restricoes": 0, "indice_inadimplencia_regiao": 0.02
    },
    "random_forest": {
        "cpf_produtor": "111.111.111-11",
        "car_propriedade": "BR-PR-1111",
        "valor_solicitado": 30000.00, "operacoes_ativas_valor": 10000.00,
        "cpf_regular": True, "car_regular": True, "divergencia_area_car": 0,
        # Score super baixo e histórico ruim para forçar o Random Forest a bloquear:
        "score_credito": 300, "solicitacoes_recusadas": 6, "historico_restricoes": 2, "indice_inadimplencia_regiao": 0.15
    },
    "aprovado": {
        "cpf_produtor": "222.222.222-22",
        "car_propriedade": "BR-PR-2222",
        "valor_solicitado": 20000.00, "operacoes_ativas_valor": 5000.00,
        "cpf_regular": True, "car_regular": True, "divergencia_area_car": 0,
        "score_credito": 850, "solicitacoes_recusadas": 0, "historico_restricoes": 0, "indice_inadimplencia_regiao": 0.01
    }
}

async def enviar_proposta(client, id_requisicao, tipo_cenario):
    payload = CENARIOS[tipo_cenario]
    try:
        start_time = time.time()
        response = await client.post(API_URL, json=payload, timeout=10.0)
        end_time = time.time()
        
        tempo_ms = (end_time - start_time) * 1000
        dados_resposta = response.json()
        
        return {
            "status": dados_resposta.get("status"),
            "tecnica": dados_resposta.get("tecnica_bloqueio", "Nenhuma"),
            "tempo": tempo_ms
        }
    except Exception as e:
        return {"status": "Erro", "tecnica": str(e), "tempo": 0}

async def rodar_teste_estresse(total_requisicoes):
    print(f"🚀 Iniciando simulação de {total_requisicoes} requisições simultâneas...")
    
    # Vamos dividir as requisições igualmente entre os cenários para gerar o "funil"
    tipos = ["especialista", "grafos", "random_forest", "aprovado"]
    
    start_total = time.time()
    
    # Criamos o cliente assíncrono HTTP
    async with httpx.AsyncClient() as client:
        tarefas = []
        for i in range(total_requisicoes):
            tipo_cenario = tipos[i % len(tipos)]
            tarefas.append(enviar_proposta(client, i, tipo_cenario))
        
        # Dispara todas ao mesmo tempo!
        resultados = await asyncio.gather(*tarefas)
        
    end_total = time.time()
    
    # 2. Contabilização dos Resultados (Métricas da Tabela)
    bloqueios_mcr = sum(1 for r in resultados if r["tecnica"] == "Sistema Especialista (Regras MCR)")
    bloqueios_grafos = sum(1 for r in resultados if "Grafo" in r["tecnica"] or "NetworkX" in r["tecnica"] or r["tecnica"] == "Rede de Grafos")
    bloqueios_rf = sum(1 for r in resultados if "Random Forest" in r["tecnica"])
    aprovados = sum(1 for r in resultados if r["status"] == "Aprovado")
    
    tempos_validos = [r["tempo"] for r in resultados if r["tempo"] > 0]
    tempo_medio = sum(tempos_validos) / len(tempos_validos) if tempos_validos else 0

    print("\n" + "="*45)
    print("📊 RELATÓRIO DO EXPERIMENTO (COMPORTAMENTO DA IA)")
    print("="*45)
    print(f"Propostas Submetidas:      {total_requisicoes}")
    print(f"Bloqueios: Sist. Especialista: {bloqueios_mcr}")
    print(f"Bloqueios: Redes de Grafos:    {bloqueios_grafos if bloqueios_grafos > 0 else 'Simulado via rota de logs'}")
    print(f"Bloqueios/Aprovações (RF):     {bloqueios_rf} Bloqueados | {aprovados} Aprovados")
    print(f"Tempo Médio de Resposta:       {tempo_medio:.2f} ms")
    print(f"Tempo Total do Experimento:    {(end_total - start_total):.2f} segundos")
    print("="*45)

if __name__ == "__main__":
    # Garante que as bibliotecas necessárias estão instaladas antes de rodar
    # pip install httpx
    asyncio.run(rodar_teste_estresse(total_requisicoes=200))
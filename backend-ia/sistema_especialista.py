# backend-ia/sistema_especista.py

def avaliar_regras_mcr(valor_solicitado, operacoes_ativas_valor, cpf_regular, car_regular):
    """
    Sistema Especialista para validação de regras determinísticas do MCR (Manual de Crédito Rural).
    Retorna se o perfil está 'Aprovado' ou 'Bloqueado', junto com os motivos.
    """
    # Limite máximo simulado pelo PROAGRO para o Ano Safra (ex: R$ 500.000,00)
    LIMITE_MAXIMO_SAFRA = 500000.00
    
    bloqueios = []

    # Regra 1: Verificação de Regularidade do CPF
    if not cpf_regular:
        bloqueios.append("CPF do produtor possui restrições ativas.")

    # Regra 2: Verificação de Regularidade do CAR (Cadastro Ambiental Rural)
    if not car_regular:
        bloqueios.append("CAR da propriedade possui pendências ou restrições ambientais.")

    # Regra 3: Verificação de estouramento de limite financeiro cumulativo
    valor_total_acumulado = operacoes_ativas_valor + valor_solicitado
    if valor_total_acumulado > LIMITE_MAXIMO_SAFRA:
        excesso = valor_total_acumulado - LIMITE_MAXIMO_SAFRA
        bloqueios.append(f"Limite do Ano Safra excedido. O valor total (R$ {valor_total_acumulado:,.2f}) "
                         f"ultrapassa o teto de R$ {LIMITE_MAXIMO_SAFRA:,.2f} em R$ {excesso:,.2f}.")

    # Decisão do Sistema Especialista
    if bloqueios:
        return {
            "status": "Bloqueado",
            "motivos": bloqueios
        }
    else:
        return {
            "status": "Aprovado",
            "motivos": ["Atende a todos os critérios de conformidade do MCR."]
        }

# --- Cenário de Teste Rápido ---
if __name__ == "__main__":
    print("--- Testando o Sistema Especialista (PROAGRO Smart) ---\n")
    
    # Simulando um produtor tentando solicitar R$ 200.000,00
    # Mas ele já tem R$ 350.000,00 em operações ativas (Total: 550.000 -> Estoura o limite!)
    resultado_teste = avaliar_regras_mcr(
        valor_solicitado=200000.00,
        operacoes_ativas_valor=350000.00,
        cpf_regular=True,
        car_regular=True
    )
    
    print(f"Resultado da Análise: {resultado_teste['status']}")
    for motivo in resultado_teste['motivos']:
        print(f"- {motivo}")
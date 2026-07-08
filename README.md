# PROAGRO Smart 🌾🤖

O **PROAGRO Smart** é uma plataforma híbrida e inteligente voltada para a automação da análise e concessão de crédito agrícola e conformidade com o PROAGRO. O sistema adota uma **Arquitetura Neuro-Simbólica em Pipeline** distribuída em microsserviços, combinando o rigor normativo das leis financeiras com a flexibilidade do aprendizado estatístico.

---

## 🏛️ Arquitetura do Sistema e Pipeline de IA

A aplicação é dividida em dois microsserviços principais que se comunicam de forma assíncrona via requisições HTTP/JSON:

1. **Back-end Orchestrator (Node.js & Express):** Responsável pelas regras de negócio da plataforma, autenticação, controle de fluxo e pela persistência robusta no banco de dados **PostgreSQL** utilizando o **Prisma ORM**.
2. **AI Inference Motor (Python & FastAPI):** Motor de alta performance dedicado exclusivamente à execução do pipeline de inteligência artificial.
3. ### O Pipeline Neuro-Simbólico (*Fail-Fast*)
Para otimizar o uso de recursos e garantir respostas em milissegundos, o motor em Python adota a estratégia de *Short-Circuit Evaluation* (Avaliação em Curto-Circuito):

* **Pilar 1: Sistema Especialista (IA Simbólica):** Avalia de forma determinística as regras de compliance baseadas no Manual de Crédito Rural (MCR) do Banco Central (limite de Ano Safra, regularidade de CPF/CAR). Se houver violação, o pipeline é interrompido imediatamente.
* **Pilar 2: Redes de Grafos (IA Simbólica):** Utiliza a biblioteca `NetworkX` para mapear relacionamentos territoriais e familiares, detectando fraudes estruturais como o fracionamento de CAR através de laranjas.
* **Pilar 3: Machine Learning (IA Subsimbólica/Neuro):** Utiliza o algoritmo `Random Forest` (previamente treinado e validado com **92,4% de acurácia**) para inferir o risco probabilístico de inadimplência com base no perfil de crédito do produtor (score, restrições e recusas históricas).

---

## 🛠️ Tecnologias Utilizadas

### Web & Persistência (Node.js)
* Node.js (v22+) & Express
* PostgreSQL 16
* Prisma ORM
* Axios (Comunicação HTTP Assíncrona)

### Inteligência Artificial & Computação (Python)
* Python 3.14+
* FastAPI & Uvicorn
* Scikit-Learn & Joblib (Random Forest)
* NetworkX (Ciência de Redes / Grafos)
* Pandas & NumPy

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Node.js instalado
* Python 3 instalado
* Instância do PostgreSQL rodando

### 1. Configuração do Banco de Dados e Node.js
Clone o repositório e acesse a pasta da plataforma web:
```bash
cd plataforma-web
Instale as dependências:

Bash
npm install
Configure o arquivo .env na raiz da pasta plataforma-web com a sua string de conexão do banco:

Snippet de código
DATABASE_URL="postgresql://usuario:senha@localhost:5432/proagro_smart?schema=public"
Execute as migrações do Prisma para estruturar o PostgreSQL:

Bash
npx prisma migrate dev
Inicie o servidor Node.js (com Nodemon):

Bash
npm run dev
O servidor web estará ativo em http://localhost:3000.

2. Configuração do Motor de IA (Python)
Abra um novo terminal e acesse a pasta do backend de inteligência artificial:

Bash
cd backend-ia
Instale os pacotes necessários:

Bash
pip install fastapi uvicorn scikit-learn joblib pandas numpy networkx httpx
Certifique-se de que o modelo treinado modelo_proagro_rf.pkl está localizado dentro da pasta models/. Caso queira gerar um novo treinamento ou testar os componentes de forma isolada, você pode rodar os scripts auxiliares:

Bash
# Para rodar os testes unitários do Sistema Especialista:
python sistema_especialista.py

# Para testar o comportamento preditivo do Random Forest via terminal:
python testar_rf.py
Inicie o servidor de inferência com o Uvicorn:

Bash
python -m uvicorn main:app --reload --port 8000
O motor de IA estará ativo na porta 8000 com documentação interativa (Swagger) disponível em http://127.0.0.1:8000/docs.

🧪 Simulação de Testes de Carga
O sistema conta com um script de estresse para simular requisições assíncronas simultâneas de agências bancárias integradas. Para rodar o experimento de concorrência e verificar o tempo médio de resposta do pipeline:

Bash
python simular_carga.py
🎓 Créditos Acadêmicos
Desenvolvido como projeto prático para a disciplina de Engenharia de Software / Sistemas com IA no curso de Engenharia de Software da Universidade Tecnológica Federal do Paraná (UTFPR) — Câmpus Cornélio Procópio.

📊 SmartReport - Analista de Dados com IA (Llama 3.3)
Este é o motor de processamento do SmartReport. Uma API robusta desenvolvida para transformar dados brutos de planilhas (CSV/XLSX) em relatórios executivos detalhados em PDF, utilizando Inteligência Artificial de última geração.

Status do Projeto: 🟢 Backend Deployado (Render)

Modelo Principal: Llama-3.3-70b-Versatile (via Groq)

🛠️ Tecnologias Utilizadas
FastAPI: Framework moderno e de alta performance para Python.

Groq Cloud (LLM): Processamento de linguagem natural ultra-rápido com Llama 3.3.

Pandas: Manipulação e sanitização de dados.

ReportLab: Geração dinâmica de documentos PDF profissionais.

Matplotlib: Criação de visualizações gráficas baseadas em métricas reais.

⚙️ Arquitetura e Diferenciais
Ao contrário de scripts simples, este backend foi estruturado seguindo boas práticas de engenharia:

Orquestração de Dados: Recebe arquivos multipart, processa via Pandas e envia apenas o contexto relevante para a IA, otimizando o uso de tokens.

Visualizer Engine: Sistema personalizado para geração de PDFs com suporte a textos justificados e inserção de gráficos em Base64.

Clean Endpoints: Separação clara entre as rotas de análise e os serviços de download de arquivos.

# Stratix Hub | Data Intelligence Ecosystem

O **Stratix Hub** é um ecossistema de análise de dados *end-to-end* projetado para transformar dados brutos em inteligência estratégica. O projeto centraliza e padroniza informações de setores distintos — Varejo, Logística e Finanças — utilizando automação de ponta e inteligência artificial para garantir a integridade da tomada de decisão.

---

## 💡 Propósito e Visão

O projeto resolve a fragmentação e a baixa qualidade de dados comuns em e-commerces e cadeias de suprimentos. O **Stratix Hub** atua na desestruturação de dados "sujos" através de três pilares:

1. **Automação Resiliente:** Ingestão contínua com tratamento de falhas e limites de API.
2. **Enriquecimento Semântico:** Uso de LLMs (Large Language Models) para traduzir ruído em informação técnica padronizada.
3. **Modelagem Eficiente:** Estrutura de dados em camadas (Medallion Architecture) para performance e clareza.

---

## 🏗️ Arquitetura da Solução

O hub utiliza uma *stack* moderna e escalável, integrando ferramentas líderes em engenharia e visualização:

* **Ingestão:** Scripts em **Python** (Selenium/Requests) com lógica de *retry* e *batch processing*.
* **Inteligência:** Integração com **Google Gemini API** para normalização de dados não estruturados.
* **Armazenamento:** Banco de Dados **PostgreSQL** (Supabase) com alta disponibilidade.
* **Transformação:** Camada de modelagem (Bronze/Silver/Gold) via **Views SQL** e **Regex**.
* **Visualização:** Dashboards dinâmicos focados em *storytelling* e métricas acionáveis.

---

## 🚀 Diferenciais Técnicos do Ecossistema

Este projeto não apenas coleta dados, ele garante a **Qualidade do Dado (Data Quality)** através de:
* **Normalização Híbrida:** Combinação de Expressões Regulares (Regex) e IA para garantir 100% de match em Joins complexos.
* **Idempotência:** Scripts projetados para serem executados múltiplas vezes sem gerar duplicatas ou inconsistências (lógica de Upsert).
* **Escalabilidade:** Processamento em lotes (*batch*) para otimização de custos e performance de API.

---

## 📂 Verticais do Hub

### 🔵 01. Tech Retail Insights (Ativo 🚀)
Módulo de monitoramento do mercado de hardware de alta performance.
* **Core:** Web scraping, de-para semântico e análise de volatilidade de preços.
* **Status:** ✅ Produção / Refinamento de Dados.

### 🟡 02. Logistics Analytics
* **Foco:** Monitoramento de SLAs, fluxos de entrega e otimização de frete.
* **Status:** ⏳ Planejamento.

### 🟢 03. Financial Control
* **Foco:** Análise de margem, fluxo de caixa e projeções.
* **Status:** ⏳ Backlog.

---

## 🛠️ Como navegar neste repositório

Cada projeto possui sua própria documentação detalhada:
1.  Acesse a pasta do projeto (ex: `/01-tech-retail`).
2.  Consulte o **README interno** para detalhes sobre a lógica de enriquecimento, esquemas de banco de dados e visualizações.
---

## 👨‍💻 Sobre o Autor

**Davi Henrick** – *Analista de Dados & BI*  
Desenvolvendo soluções que conectam tecnologia, dados e estratégia de negócios.

---
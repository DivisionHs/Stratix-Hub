# 🔵 Tech Retail Insights | Stratix Hub

Este módulo é o motor de inteligência de mercado do Stratix Hub, focado na extração e normalização de dados do varejo de hardware de alta performance. O foco atual é a análise de CPUs, transformando descrições caóticas de e-commerce em especificações técnicas precisas.

---

## 🎯 Desafios Técnicos & Soluções

O maior desafio deste projeto não foi coletar os dados, mas sim **garantir a integridade do cruzamento de informações (Join Integrity)**. 

### 1. Inteligência Semântica com LLM (Gemini API)
Diferente de scrapers comuns, este módulo utiliza IA para traduzir codinomes comerciais em modelos técnicos:
* **Entrada:** `"Processador Intel Core I3 21xx, LGA 1155 - Oem"`
* **Processamento:** A IA identifica a família e traduz para **`Intel Core i3 2100`**.
* **Saída:** Dados estruturados de soquete (LGA 1155), núcleos (2) e clock base.

### 2. Match de Alta Precisão (Regex & Word Boundaries)
Para evitar "falsos positivos" (como confundir um `i5 14400` com um `i5 14400F`), implementamos uma lógica de comparação em nível de banco de dados (SQL):
* **Normalização Híbrida:** Remoção dinâmica de hífens e espaços apenas no momento do cruzamento.
* **Regex Boundaries (`\y`):** Garantia de que o modelo seja uma "palavra inteira", impedindo que um modelo menor dê match em uma variante mais robusta por acidente.

---

## ⚙️ Arquitetura de Dados (Pipeline)

O projeto segue o fluxo de processamento de dados moderno:

1.  **Bronze (Staging):** Dados brutos extraídos via Selenium da Kabum, preservando a string original do anúncio.
2.  **Silver (Enriched):** Processamento via script de enriquecimento que consulta a API do Gemini em lotes (*batch*) de 10 itens.
3.  **Gold (Analytical):** View final que consolida preços, links e especificações técnicas limpas, pronta para consumo no Power BI.

---

## 🛠️ Stack Tecnológica

* **Ingestão:** Python (Selenium) + Lógica de Retry (Exponencial Backoff).
* **IA:** Google Gemini 3.1 Flash Lite (Normalização de Nomenclatura).
* **Banco de Dados:** PostgreSQL (Supabase) com uso intensivo de **Regular Expressions** e **Views**.
* **BI:** Power BI para visualização de Market Share e Performance/Preço.

---

## 🚀 Como Executar o Enriquecimento

O script de enriquecimento (`enrichment.py`) é resiliente a falhas de rede e limites de cota:
1.  O script identifica automaticamente produtos sem referência técnica no banco.
2.  Processa os dados em lotes para otimizar o uso da API.
3.  Em caso de erro de servidor (503), aplica uma lógica de 3 tentativas antes de pular para o próximo lote, garantindo que nenhum dado seja perdido.

```bash
# Executar o enriquecimento de dados
python src/enrichment.py
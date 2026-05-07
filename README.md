# Stratix Hub | Data Intelligence Ecosystem

O **Stratix Hub** é um ecossistema de análise de dados *end-to-end* projetado para transformar dados brutos em inteligência estratégica. A ideia nasceu da necessidade de centralizar e padronizar informações de setores distintos — Varejo, Logística e Finanças — permitindo uma visão clara e acionável para a tomada de decisão.

---

## 💡 A Origem e o Propósito

O projeto surgiu ao observar a fragmentação de dados em e-commerces e cadeias de suprimentos. Muitas vezes, as informações estão disponíveis, mas "sujas", desestruturadas e espalhadas entre diferentes plataformas. 

O **Stratix Hub** resolve essa dor através de três pilares:
1. **Automação:** Eliminação da coleta manual, garantindo dados sempre atualizados.
2. **Padronização:** Aplicação de regras de negócio via SQL para normalizar marcas e categorias.
3. **Acessibilidade:** Entrega de dashboards intuitivos que respondem perguntas de negócio em segundos.

---

## 🏗️ Arquitetura Geral da Solução

O hub utiliza uma *stack* moderna e escalável, integrando as melhores ferramentas de engenharia e visualização:

* **Ingestão:** Scripts em **Python** (Selenium) para automação de *web scraping* em tempo real.
* **Armazenamento:** Banco de Dados **PostgreSQL** hospedado na nuvem via **Supabase**.
* **Transformação:** Camada de modelagem (Bronze/Silver/Gold) construída com **Views SQL** para limpeza e tratamento.
* **Visualização:** **Power BI** para *storytelling* e exploração analítica.

---

## 📂 Verticais do Hub

Abaixo estão os módulos que compõem o ecossistema. Cada um possui seu próprio ciclo de vida e documentação específica.

### 🔵 01. Tech Retail Insights (MVP Ativo)
Focado no mercado de hardware e eletrônicos, este módulo monitora preços e disponibilidade de componentes de alta performance.
* **Objetivo:** Identificar janelas de oportunidade de compra e analisar o *market share* de fabricantes.
* **Diferencial:** Lógica de classificação avançada que separa fabricantes de "chips" de montadoras finais.
* **Status:** ⏳ **Em desenvolvimento** (Fase de Modelagem de Dados)

### 🟡 02. Logistics Analytics
* **Foco:** Monitoramento de fluxos de entrega, cumprimento de SLAs e otimização de custos de frete.
* **Status:** ⏳ **Backlog** (Fase de Planejamento)

### 🟢 03. Financial Control
* **Foco:** Análise de margem de contribuição, fluxo de caixa e projeções financeiras.
* **Status:** ⏳ **Backlog** (Fase de Planejamento)

---

## 🛠️ Como navegar neste repositório

Cada pasta de projeto possui sua própria documentação detalhada e instruções de execução:
1.  Acesse a pasta do projeto desejado (ex: `/01-tech-retail`).
2.  Consulte o **README interno** para entender as particularidades técnicas, requisitos e como reproduzir o ambiente.

---

## 👨‍💻 Sobre o Autor

**Davi Henrick** – *Analista de Dados & BI*  
Desenvolvendo soluções que conectam tecnologia, dados e estratégia de negócios.

---
# 🔵 Tech Retail Insights | Stratix Hub

Este módulo é focado na extração, tratamento e análise de dados do mercado de hardware e eletrônicos. O objetivo principal é monitorar a flutuação de preços e a disponibilidade de componentes de alta performance (CPUs, GPUs, RAM e SSDs) no varejo brasileiro.

---

## 🎯 Objetivo do Projeto

Transformar dados não estruturados provenientes de e-commerces em um dashboard analítico capaz de:
* Identificar o **Market Share** visual de fabricantes por categoria.
* Calcular o **Desconto Real** (diferença entre preço parcelado e à vista).
* Monitorar o **Ticket Médio** de cada categoria de produto em tempo real.

---

## 📂 Estrutura de Pastas

* **`/src`**: Contém o motor de ingestão em Python.
    * `main.py`: Script principal de execução do scraping.
    * `database.py`: Módulo de conexão e persistência de dados no PostgreSQL/Supabase.
    * `utils.py`: Funções auxiliares de limpeza de dados e configuração do driver Selenium.
* **`/sql`**: Scripts SQL de DDL (Data Definition Language) e criação de Views analíticas.
* **`/dashboards`**: Arquivo `.pbix` com a camada de visualização final.

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagem:** Python 3.x
* **Automação:** Selenium WebDriver
* **Banco de Dados:** PostgreSQL (Supabase Cloud)
* **Modelagem de Dados:** SQL (Views para Camada Silver)
* **BI:** Power BI

---

## ⚙️ Regras de Negócio e Tratamento (Camada Silver)

Um dos maiores desafios técnicos deste módulo foi a **normalização dos fabricantes**. Como os títulos dos produtos no varejo são inconsistentes, foi implementada uma lógica de `CASE WHEN` em SQL para:
1. **Priorização de Marcas:** Identificar marcas de módulos (ex: Kingston, Corsair, Rise Mode).
2. **Blindagem de Chipsets:** Garantir que termos como "NVIDIA" ou "AMD" só sejam atribuídos como fabricantes em categorias de GPU ou CPU, evitando falsos positivos em memórias RAM "compatíveis com NVIDIA".

---

## 🚀 Como Executar

1. **Pré-requisitos:**
   * Python instalado.
   * WebDriver compatível com seu navegador (ex: ChromeDriver).

2. **Configuração:**
   * Renomeie o arquivo `.env.example` para `.env`.
   * Preencha suas credenciais de acesso ao banco de dados PostgreSQL.

   3. **Execução:**
      ```bash
      pip install -r requirements.txt
      python src/main.py

---

# 📊 Visualização

O dashboard final consome as **Views SQL** criadas no Supabase, garantindo que o Power BI receba dados já limpos e pré-processados, otimizando a performance do relatório.

---
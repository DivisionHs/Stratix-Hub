import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Importações dos módulos internos (Garanta que o utils.py já esteja com a nova limpeza)
from utils import remover_acentos, limpar_monetario
from database import salvar_no_supabase


def configurar_navegador():
    """
    Inicializa o WebDriver do Chrome com argumentos de performance.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Descomente para rodar sem abrir a janela
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def executar_scraping_categoria(driver, config):
    """
    Executa o ciclo de extração para uma categoria específica do hardware.

    Args:
        driver: Instância do Selenium WebDriver.
        config (dict): Dicionário contendo 'keyword', 'url_base' e 'tabela'.

    Returns:
        pd.DataFrame: Dados limpos da categoria processada.
    """
    lista_scraping = []

    print(f"\n📂 Iniciando Categoria: {config['tabela'].upper()}")

    for pagina in range(1, 6):
        # Constrói a URL com paginação
        url = f"{config['url_base']}?page_number={pagina}&page_size=60&sort=most_searched"
        print(f"🔗 [{pagina}/5] Navegando para: {url}")
        driver.get(url)
        time.sleep(5)

        elementos = driver.find_elements(By.CSS_SELECTOR, 'main a[aria-label]')

        for i, item in enumerate(elementos, 1):
            texto_bruto = item.get_attribute('aria-label').strip()
            texto_teste = remover_acentos(texto_bruto.lower())

            # Filtro dinâmico baseado na palavra-chave da categoria
            if texto_teste.startswith(config['keyword']):

                # Regex para encontrar valores monetários e multiplicador de parcelas
                precos = re.findall(r"R\$\s?(\d+(?:\.\d+)*(?:,\d+)?|(?:\d+\.?\d*))", texto_bruto)
                match_p = re.search(r"(\d+)x\s?de", texto_bruto)
                num_p = int(match_p.group(1)) if match_p else 1

                # Cálculo dos preços (Promocional vs Original)
                if len(precos) >= 2:
                    v_pix = limpar_monetario(precos[0])
                    v_total_p = round(limpar_monetario(precos[1]) * num_p, 2)
                else:
                    v_pix = limpar_monetario(precos[0]) if precos else 0.0
                    v_total_p = v_pix

                # Extração e limpeza do nome do produto
                nome = texto_bruto.split("R$")[0].split(", avaliação")[0].strip().rstrip(',')

                lista_scraping.append({
                    "nome_produto": nome,
                    "preco_promocional": v_pix,
                    "preco_original": v_total_p,
                    "link_produto": item.get_attribute('href'),
                    "data_extracao": pd.Timestamp.now()
                })

            if i % 20 == 0 or i == len(elementos):
                print(f"  ⚡ Processados {i}/{len(elementos)} itens da página...")

    return pd.DataFrame(lista_scraping)


def main():
    """
    Orquestrador principal: gerencia a lista de categorias e o fluxo de carga no Supabase.
    """
    # Configurações das categorias monitoradas pelo Stratix Hub
    categorias = [
        {
            "keyword": "placa de video",
            "url_base": "https://www.kabum.com.br/hardware/placa-de-video-vga",
            "tabela": "stg_kabum_gpus"
        },
        {
            "keyword": "processador",
            "url_base": "https://www.kabum.com.br/hardware/processadores",
            "tabela": "stg_kabum_cpus"
        },
        {
            "keyword": "memoria",
            "url_base": "https://www.kabum.com.br/hardware/memoria-ram",
            "tabela": "stg_kabum_ram"
        },
        {
            "keyword": "ssd",
            "url_base": "https://www.kabum.com.br/hardware/ssd-2-5",
            "tabela": "stg_kabum_ssd"
        }
    ]

    driver = configurar_navegador()

    try:
        for cat in categorias:
            # Chama a função de extração para a categoria atual
            df_bruto = executar_scraping_categoria(driver, cat)

            # Filtragem de segurança: remove produtos sem preço original (esgotados ou falha)
            df_limpo = df_bruto[df_bruto['preco_original'] > 0].copy()

            # Relatório visual no console
            print("\n" + "=" * 45)
            print(f"📊 RELATÓRIO: {cat['tabela'].upper()}")
            print("=" * 45)
            print(f"📦 Brutos lidos:   {len(df_bruto)}")
            print(f"🧹 Filtrados:      {len(df_bruto) - len(df_limpo)} (inválidos)")
            print(f"✨ Prontos p/ Carga: {len(df_limpo)}")

            # Integração com o módulo database.py
            status = salvar_no_supabase(df_limpo, cat['tabela'])
            print(f"🚀 Status Banco:   {status}")
            print("=" * 45)

    except Exception as e:
        print(f"❌ Erro fatal durante a orquestração: {e}")
    finally:
        print("\n🏁 Finalizando motor de busca...")
        driver.quit()


if __name__ == "__main__":
    main()
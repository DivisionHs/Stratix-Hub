import os
import json
import time
import re
from google import genai
from dotenv import load_dotenv
from database import buscar_produtos_sem_referencia, salvar_referencia_ia

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# Utilizando o modelo 1.5-flash para maior estabilidade no plano gratuito
MODEL_ID = "gemini-3.1-flash-lite"


def padronizar_soquete(soquete_raw):
    """
    Normaliza soquetes para padrões de mercado (LGA com espaço, AM/FM sem espaço).
    """
    if not soquete_raw:
        return None

    s = str(soquete_raw).upper()
    s = re.sub(r'\(.*\)', '', s).strip()

    # 1. Se for soquete AMD (AM ou FM), garante que fiquem juntos (Ex: AM4)
    if re.match(r'^(AM|FM)\d+', s.replace(' ', '')):
        return s.replace(' ', '')

    # 2. Se for soquete Intel antigo (Socket P / PGA478)
    if any(x in s for x in ['PGA478', 'SOCKET P', 'PGA 478']):
        return 'PGA 478'

    # 3. Para LGA e outros que não sejam AM/FM, garante o espaço (Ex: LGA 1700)
    if not s.startswith(('AM', 'FM')):
        s = re.sub(r'([A-Z]+)(\d+)', r'\1 \2', s)

    # 4. Limpezas finais
    s = s.replace('SOCKET', '').replace('FCLGA', 'LGA').strip()
    s = re.sub(r'\s+', ' ', s)

    return s


def extrair_dados_com_ia_em_lote():
    produtos_pendentes = buscar_produtos_sem_referencia()

    if not produtos_pendentes:
        print("😴 Nenhuma nova CPU pendente.")
        return

    tamanho_lote = 10
    lotes = [produtos_pendentes[i:i + tamanho_lote] for i in range(0, len(produtos_pendentes), tamanho_lote)]

    # Cálculo do total de itens para o print
    total_itens = len(produtos_pendentes)
    total_lotes = len(lotes)

    print(f"🤖 IA Stratix: Iniciando processamento total.")
    print(f"📊 Volume: {total_itens} produtos únicos identificados em {total_lotes} lotes de {tamanho_lote}.")
    print("-" * 50)

    for i, lote in enumerate(lotes):
        # Mostra o progresso percentual ou fracionado
        print(f"📦 Lote {i + 1}/{total_lotes} | Processando agora: {len(lote)} itens...")
        lista_formatada = "\n".join([f"{j + 1}. {nome}" for j, nome in enumerate(lote)])

        prompt = f"""
        Você é um Especialista em Hardware sênior. Converta nomes de anúncios em Nomes Comerciais Padronizados para Dashboards.

        REGRAS DE OURO PARA "modelo_referencia":
        1. Use o nome comercial completo e elegante (Ex: "Intel Core i5 12400F", "AMD Ryzen 7 9700X").
        2. Converta siglas: "R7", "R5" -> "AMD Ryzen 7", "AMD Ryzen 5".
        3. Identifique o modelo real em nomes genéricos (Ex: "I3 21xx" -> "Intel Core i3 2100").
        4. NUNCA use Part Numbers (BX..., 100-...) ou termos de venda (OEM, TRAY, S/ COOLER).
        5. PREENCHIMENTO TOTAL: Identifique soquete, núcleos e clock base com base no seu conhecimento técnico.

        PRODUTOS:
        {lista_formatada}

        Retorne apenas a LISTA JSON: modelo_referencia, fabricante, soquete, qtd_nucleos, qtd_threads, clock_ghz, tem_video_integrado.
        """

        max_tentativas = 3
        for tentativa in range(max_tentativas):
            try:
                response = client.models.generate_content(model=MODEL_ID, contents=prompt)
                res_text = response.text

                start = res_text.find('[')
                end = res_text.rfind(']') + 1
                if start == -1 or end == 0:
                    raise ValueError("JSON não encontrado")

                lista_specs = json.loads(res_text[start:end])

                for specs in lista_specs:
                    # Limpeza de caracteres especiais que a IA pode inventar no final (pontos, etc)
                    raw_modelo = specs.get('modelo_referencia', '')
                    specs['modelo_referencia'] = re.sub(r'[^\w\s-]', '', str(raw_modelo)).strip()

                    specs['fabricante'] = str(specs.get('fabricante', '')).upper().strip()
                    specs['soquete'] = padronizar_soquete(specs.get('soquete'))

                    # Garantia de Tipos Numéricos e Limpeza de Clock
                    try:
                        specs['qtd_nucleos'] = int(specs.get('qtd_nucleos')) if specs.get('qtd_nucleos') else None
                        specs['qtd_threads'] = int(specs.get('qtd_threads')) if specs.get('qtd_threads') else None

                        clock_raw = str(specs.get('clock_ghz', '')).replace(',', '.')
                        match_clock = re.search(r'(\d+\.?\d*)', clock_raw)
                        specs['clock_ghz'] = float(match_clock.group(1)) if match_clock else None
                    except:
                        specs['clock_ghz'] = None

                    salvar_referencia_ia(specs)

                print(f"✅ Lote processado. {len(lista_specs)} itens integrados ao novo Depara.")
                time.sleep(6)  # Tempo de segurança para o plano gratuito
                break

            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e).upper():
                    espera = (tentativa + 1) * 12
                    print(f"⏳ Servidor ocupado. Tentativa {tentativa + 1}. Aguardando {espera}s...")
                    time.sleep(espera)
                else:
                    print(f"❌ Erro no lote: {e}")
                    break


if __name__ == "__main__":
    extrair_dados_com_ia_em_lote()
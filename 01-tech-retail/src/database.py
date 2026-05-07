import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as credenciais do arquivo .env
load_dotenv()


def salvar_no_supabase(df_novo, tabela_alvo):
    """
    Realiza a carga de dados no Supabase utilizando SQLAlchemy.

    A função compara o que está sendo enviado com o que já existe no banco
    através de uma chave composta (link + preço), garantindo que apenas
    novos produtos ou alterações de preços sejam registrados.

    Args:
        df_novo (pd.DataFrame): DataFrame com os dados raspados.
        tabela_alvo (str): Nome da tabela no banco (ex: 'stg_kabum_gpus').

    Returns:
        str: Mensagem de status da operação.
    """
    db_url = os.getenv('SUPABASE_URL')
    db_engine = create_engine(db_url)

    if df_novo.empty:
        return "⚠️ DataFrame vazio. Operação abortada."

    with db_engine.connect() as conn:
        try:
            # Tenta ler os dados atuais para evitar duplicidade
            query = f"SELECT link_produto, preco_promocional FROM {tabela_alvo}"
            df_existente = pd.read_sql(query, con=conn)

            # Criação de chaves únicas temporárias para comparação
            df_novo['check'] = df_novo['link_produto'] + df_novo['preco_promocional'].map('{:.2f}'.format)
            df_existente['check'] = df_existente['link_produto'] + df_existente['preco_promocional'].map(
                '{:.2f}'.format)

            # Filtra apenas registros que não constam no banco
            df_final = df_novo[~df_novo['check'].isin(df_existente['check'])].drop(columns=['check'])
        except Exception:
            # Caso a tabela ainda não exista, envia o DataFrame completo
            df_final = df_novo
            print(f"ℹ️ Tabela {tabela_alvo} não detectada. Iniciando carga total...")

        if not df_final.empty:
            # Envia os dados para o Supabase (camada Bronze)
            df_final.to_sql(tabela_alvo, con=conn, if_exists='append', index=False)
            conn.commit()
            return f"✅ Sucesso: {len(df_final)} novos registros inseridos."

        return "😴 Sincronização ok: Nenhum novo preço detectado."
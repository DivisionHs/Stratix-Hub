import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carrega as credenciais do arquivo .env
load_dotenv()


def get_engine():
    """ Auxiliar para gerenciar a conexão com o banco utilizando a URL do .env """
    db_url = os.getenv('SUPABASE_URL')
    if not db_url:
        raise ValueError("⚠️ A variável SUPABASE_URL não foi encontrada no arquivo .env")
    return create_engine(db_url)


def salvar_no_supabase(df_novo, tabela_alvo):
    """
    Realiza a carga de dados no Supabase utilizando SQLAlchemy.

    A função compara o que está sendo enviado com o que já existe no banco
    através de uma chave composta (link + preço), garantindo que apenas
    novos produtos ou alterações de preços sejam registrados.
    """
    db_engine = get_engine()

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


def buscar_produtos_sem_referencia():
    engine = get_engine()
    # Esta query agora é mais rigorosa: busca vazios E incompletos
    query = """
            SELECT DISTINCT s.nome_produto
            FROM stg_kabum_cpus s
                     LEFT JOIN vw_silver_cpus v ON s.id = v.id
            WHERE v.modelo_referencia IS NULL; \
            """

    with engine.connect() as conn:
        df = pd.read_sql(query, con=conn)
        return df['nome_produto'].tolist()


def salvar_referencia_ia(dados_ia):
    engine = get_engine()
    df_ref = pd.DataFrame([dados_ia])

    with engine.connect() as conn:
        try:
            # Usamos o 'upsert' (no SQLAlchemy para PostgreSQL/Supabase)
            # Para simplificar, vamos deletar o modelo antigo e inserir o novo e completo
            modelo = dados_ia['modelo_referencia']
            conn.execute(text(f"DELETE FROM dim_cpu_reference WHERE modelo_referencia = '{modelo}'"))

            df_ref.to_sql('dim_cpu_reference', con=conn, if_exists='append', index=False)
            conn.commit()
            print(f"✅ Dados atualizados/completos: {modelo}")
        except Exception as e:
            print(f"ℹ️ Erro ao atualizar {dados_ia['modelo_referencia']}: {e}")
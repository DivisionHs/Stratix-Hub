-- Estrutura da Tabela de Referência (Dimensão)
CREATE TABLE IF NOT EXISTS dim_cpu_reference (
    modelo_referencia TEXT PRIMARY KEY,
    fabricante TEXT,
    soquete TEXT,
    qtd_nucleos INTEGER,
    qtd_threads INTEGER,
    clock_ghz DECIMAL,
    tem_video_integrado TEXT,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
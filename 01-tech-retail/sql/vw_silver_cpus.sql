-- View Silver: Une a Staging com o Depara usando Inteligência de Regex
CREATE OR REPLACE VIEW vw_silver_cpus AS
SELECT DISTINCT ON (s.nome_produto)
    s.id,
    'CPU' as categoria,
    s.nome_produto,
    d.modelo_referencia,
    d.fabricante,
    d.soquete,
    d.qtd_nucleos,
    d.qtd_threads,
    d.clock_ghz,
    d.tem_video_integrado,
    s.preco_promocional,
    s.preco_original,
    s.link_produto,
    s.data_extracao
FROM stg_kabum_cpus s
LEFT JOIN dim_cpu_reference d
    ON
    -- Match preciso ignorando hífens/espaços e respeitando limites de palavras (\y)
    REPLACE(UPPER(s.nome_produto), '-', ' ') ~* ('\y' || REPLACE(UPPER(d.modelo_referencia), '-', ' ') || '\y')
ORDER BY s.nome_produto, LENGTH(d.modelo_referencia) DESC;
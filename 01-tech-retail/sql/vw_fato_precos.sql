-- Criamos a view com a lógica de fabricante otimizada para o Stratix Hub
CREATE VIEW vw_fato_precos AS
SELECT
    categoria,
    nome_produto,
    CASE
        -- --- PRIORIDADE 1: Marcas Específicas de RAM e SSD (Evita falso positivo de NVIDIA/AMD) ---
        WHEN LOWER(nome_produto) LIKE '%kingston%' OR LOWER(nome_produto) LIKE '%fury%' THEN 'KINGSTON'
        WHEN LOWER(nome_produto) LIKE '%rise mode%' THEN 'RISE MODE'
        WHEN LOWER(nome_produto) LIKE '%husky%' THEN 'HUSKY'
        WHEN LOWER(nome_produto) LIKE '%corsair%' OR LOWER(nome_produto) LIKE '%vengeance%' THEN 'CORSAIR'
        WHEN LOWER(nome_produto) LIKE '%adata%' OR LOWER(nome_produto) LIKE '%xpg%' THEN 'ADATA/XPG'
        WHEN LOWER(nome_produto) LIKE '%crucial%' THEN 'CRUCIAL'
        WHEN LOWER(nome_produto) LIKE '%lexar%' THEN 'LEXAR'
        WHEN LOWER(nome_produto) LIKE '%dale7%' THEN 'DALE7'
        WHEN LOWER(nome_produto) LIKE '%wd%' OR LOWER(nome_produto) LIKE '%western digital%' THEN 'WESTERN DIGITAL'
        WHEN LOWER(nome_produto) LIKE '%sandisk%' THEN 'SANDISK'
        WHEN LOWER(nome_produto) LIKE '%hiksemi%' THEN 'HIKSEMI'
        WHEN LOWER(nome_produto) LIKE '%keepdata%' THEN 'KEEPDATA'
        WHEN LOWER(nome_produto) LIKE '%win memory%' OR LOWER(nome_produto) LIKE '%winmemory%' THEN 'WINMEMORY'
        WHEN LOWER(nome_produto) LIKE '%netac%' THEN 'NETAC'
        WHEN LOWER(nome_produto) LIKE '%pny%' THEN 'PNY'
        WHEN LOWER(nome_produto) LIKE '%asgard%' THEN 'ASGARD'
        WHEN LOWER(nome_produto) LIKE '%oxybr%' THEN 'OXYBR'
        WHEN LOWER(nome_produto) LIKE '%dell%' THEN 'DELL'

        -- --- PRIORIDADE 2: Fabricantes de Chipset (Focado em GPU e CPU) ---
        -- Identifica NVIDIA apenas se não foi capturado pelas marcas acima
        WHEN (LOWER(nome_produto) LIKE '%nvidia%' OR LOWER(nome_produto) LIKE '%geforce%'
              OR LOWER(nome_produto) LIKE '%rtx%' OR LOWER(nome_produto) LIKE '%gtx%')
              AND categoria IN ('GPU', 'CPU') THEN 'NVIDIA'

        -- Identifica AMD apenas se não foi capturado pelas marcas acima
        WHEN (LOWER(nome_produto) LIKE '%amd%' OR LOWER(nome_produto) LIKE '%ryzen%'
              OR LOWER(nome_produto) LIKE '%radeon%' OR LOWER(nome_produto) LIKE '%rx %')
              AND categoria IN ('GPU', 'CPU') THEN 'AMD'

        -- Identifica INTEL
        WHEN LOWER(nome_produto) LIKE '%intel%' OR LOWER(nome_produto) LIKE '%core i%' THEN 'INTEL'

        ELSE 'Outros'
    END AS fabricante,
    preco_promocional,
    preco_original,
    link_produto,
    data_extracao
FROM (
    SELECT 'GPU' as categoria, nome_produto, preco_promocional, preco_original, link_produto, data_extracao FROM stg_kabum_gpus
    UNION ALL
    SELECT 'CPU' as categoria, nome_produto, preco_promocional, preco_original, link_produto, data_extracao FROM stg_kabum_cpus
    UNION ALL
    SELECT 'RAM' as categoria, nome_produto, preco_promocional, preco_original, link_produto, data_extracao FROM stg_kabum_ram
    UNION ALL
    SELECT 'SSD' as categoria, nome_produto, preco_promocional, preco_original, link_produto, data_extracao FROM stg_kabum_ssd
) as bronze_unificada;
-- Panorama das IES publicas federais (UFs) que ofertam licenciatura, comparando 2014 e 2024:
-- matriculas (totais e por modalidade), numero de cursos, campus presenciais e polos EaD
-- (proprios x UAB). Uma linha por IES por ano_censo (2014 e 2024).
--
-- v2: versao anterior deste script trazia so um "ultimo ano ofertado" por modalidade (uma
-- unica linha por IES, sem filtro de ano). Reescrito para o modelo ano-a-ano usado em
-- sqls/cap5/gerar_excel_resumo_todas_ies_v3.py, que compara 2014 x 2024 diretamente -- isso
-- e o que permite um filtro de ano na interface.
--
-- Polos UAB x EaD proprio sao distinguidos pelo flag superior_curso.fl_uab (S/N) do proprio
-- curso no censo, nao por um join de municipio/ano contra superior_uab_censo (essa tabela nao
-- tem qt_mat e cobre um subconjunto dos municipios que ja aparecem com matricula real via
-- fl_uab='S' -- ver web_app/content_export/export_lic_ies_geral.py).
WITH base AS (
    SELECT DISTINCT i.codigo AS ies_codigo, i.nome AS ies_nome, i.sigla, i.estado
    FROM superior_ies i
    WHERE i.categoria = 1
      AND i.org_academica = 1
      AND i.nome NOT LIKE 'Universidade codigo%'
      AND i.codigo IN (SELECT DISTINCT ies FROM superior_curso_censo WHERE tp_grau_academico = 2)
),
anos AS (
    SELECT 2014 AS ano_censo
    UNION ALL
    SELECT 2024
),
metricas AS (
    SELECT
        cc.ies,
        cc.ano_censo,
        SUM(cc.qt_mat) AS total_matriculas,
        SUM(CASE WHEN cc.tp_grau_academico = 2 THEN cc.qt_mat ELSE 0 END) AS total_matriculas_lic,
        COUNT(DISTINCT CASE WHEN cc.tp_grau_academico = 2 THEN cc.curso END) AS num_cursos_lic,
        COUNT(DISTINCT CASE WHEN cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 1 THEN cc.municipio END) AS num_campus_presencial,
        COUNT(DISTINCT CASE WHEN cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'N' THEN cc.municipio END) AS num_polos_ead_proprio,
        COUNT(DISTINCT CASE WHEN cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'S' THEN cc.municipio END) AS num_polos_uab,
        SUM(CASE WHEN cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 1 THEN cc.qt_mat ELSE 0 END) AS mat_lic_presencial,
        SUM(CASE WHEN cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'N' THEN cc.qt_mat ELSE 0 END) AS mat_lic_ead_proprio,
        SUM(CASE WHEN cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'S' THEN cc.qt_mat ELSE 0 END) AS mat_lic_uab
    FROM superior_curso_censo cc
    JOIN superior_curso c ON c.codigo = cc.curso
    WHERE cc.ano_censo IN (2014, 2024)
    GROUP BY cc.ies, cc.ano_censo
)
SELECT
    b.ies_nome,
    b.sigla,
    b.estado,
    a.ano_censo,
    COALESCE(m.total_matriculas, 0) AS total_matriculas,
    COALESCE(m.total_matriculas_lic, 0) AS total_matriculas_lic,
    COALESCE(m.num_cursos_lic, 0) AS num_cursos_lic,
    COALESCE(m.num_campus_presencial, 0) AS num_campus_presencial,
    COALESCE(m.num_polos_ead_proprio, 0) AS num_polos_ead_proprio,
    COALESCE(m.num_polos_uab, 0) AS num_polos_uab,
    COALESCE(m.mat_lic_presencial, 0) AS mat_lic_presencial,
    COALESCE(m.mat_lic_ead_proprio, 0) AS mat_lic_ead_proprio,
    COALESCE(m.mat_lic_uab, 0) AS mat_lic_uab
FROM base b
CROSS JOIN anos a
LEFT JOIN metricas m ON m.ies = b.ies_codigo AND m.ano_censo = a.ano_censo
ORDER BY b.estado, b.ies_nome, a.ano_censo;

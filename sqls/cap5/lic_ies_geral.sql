-- Panorama geral das IES publicas federais (UFs) que ofertam licenciatura: presenca por
-- modalidade (presencial/EaD/UAB), abrangencia territorial (municipios/polos) e matriculas.
--
-- OBS: os nomes de tabela usam o prefixo "superior_" porque e assim que elas existem hoje
-- em bdados/INEP.db (ver modelos_dados/*_models.py). Uma versao anterior deste script usava
-- os nomes antigos sem prefixo (ies, curso_censo, uab_censo), que nao existem mais no banco
-- atual e por isso nunca chegaram a gerar a planilha.
WITH base AS (
    -- Sua consulta original (incluindo o ID da IES para fazer os joins)
    SELECT DISTINCT
        i.codigo AS ies_codigo,
        i.nome AS ies_nome,
        i.sigla,
        i.estado
    FROM superior_ies i
    LEFT JOIN superior_uab_censo uc ON i.codigo = uc.ies
                           AND uc.tp_grau_academico = 2
                           AND uc.ano_censo > 2013
    WHERE i.categoria = 1
      AND i.org_academica = 1
      AND i.nome NOT LIKE 'Universidade codigo%'
),
-- a) Qual o ultimo ano que cada registro de Ies ofertou algum curso de licenciatura presencial
ult_ano_presencial AS (
    SELECT ies, MAX(ano_censo) as ult_ano
    FROM superior_curso_censo
    WHERE tp_grau_academico = 2 AND tp_modalidade_ensino = 1
    GROUP BY ies
),
-- b) A qtde de municipios que a ies esteve neste último ano nesta modalidade
mun_presencial_ult_ano AS (
    SELECT c.ies, COUNT(DISTINCT c.municipio) as qtd_mun_presencial, COUNT(DISTINCT c.curso) as qtd_cursos_presencial
    FROM superior_curso_censo c
    JOIN ult_ano_presencial u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
    WHERE c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 1
    GROUP BY c.ies
),
-- c) Qual o ultimo ano que cada registro de Ies ofertou algum curso de licenciatura EaD
ult_ano_ead AS (
    SELECT ies, MAX(ano_censo) as ult_ano
    FROM superior_curso_censo
    WHERE tp_grau_academico = 2 AND tp_modalidade_ensino = 2
    GROUP BY ies
),
-- d) A qtde de municipios que a ies esteve neste último ano nesta modalidade EaD
mun_ead_ult_ano AS (
    SELECT c.ies, COUNT(DISTINCT c.municipio) as qtd_mun_ead, COUNT(DISTINCT c.curso) as qtd_cursos_ead
    FROM superior_curso_censo c
    JOIN ult_ano_ead u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
    WHERE c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 2
    GROUP BY c.ies
),
-- e) Qual o ultimo ano que cada registro de Ies ofertou algum curso por uab (uab_censo) de licenciatura presencial / ativo
ult_ano_uab AS (
    SELECT ies, MAX(ano_censo) as ult_ano
    FROM superior_uab_censo
    WHERE tp_grau_academico = 2 AND situacao_polo = 'Ativo'
    GROUP BY ies
),
-- f) A qtde de polos c (count de id_polo) que estes cursos foram ofertados no ultimo ano
polos_uab_ult_ano AS (
    SELECT c.ies, COUNT(DISTINCT c.id_polo) as qtd_polos_uab, COUNT(DISTINCT c.nm_curso) as qtd_cursos_uab
    FROM superior_uab_censo c
    JOIN ult_ano_uab u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
    WHERE c.tp_grau_academico = 2 AND c.situacao_polo = 'Ativo'
    GROUP BY c.ies
),
-- g) Total de matriculas (qt_mat) no censo mais recente (2024): geral da IES, geral de
--    licenciatura e a licenciatura EaD decomposta em polo proprio x polo UAB (join pelo
--    trio ies/ano_censo/municipio contra os polos ativos da UAB naquele ano)
matriculas_2024 AS (
    SELECT
        c.ies,
        SUM(c.qt_mat) AS tot_mat,
        SUM(CASE WHEN c.tp_grau_academico = 2 THEN c.qt_mat ELSE 0 END) AS tot_mat_lic,
        SUM(CASE WHEN c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 2 AND u.municipio IS NULL THEN c.qt_mat ELSE 0 END) AS tot_mat_lic_ead_proprios,
        SUM(CASE WHEN c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 2 AND u.municipio IS NOT NULL THEN c.qt_mat ELSE 0 END) AS tot_mat_lic_ead_uab
    FROM superior_curso_censo c
    LEFT JOIN (
        SELECT DISTINCT ies, ano_censo, municipio
        FROM superior_uab_censo
        WHERE tp_grau_academico = 2
    ) u ON c.ies = u.ies AND c.ano_censo = u.ano_censo AND c.municipio = u.municipio
    WHERE c.ano_censo = 2024
    GROUP BY c.ies
)
-- Junção de todas as métricas com a base
SELECT
    b.ies_nome,
    b.sigla,
    b.estado,
    up.ult_ano AS a_ultimo_ano_presencial,
    COALESCE(mp.qtd_mun_presencial, 0) AS b_qtd_mun_presencial,
    COALESCE(mp.qtd_cursos_presencial, 0) AS b_qtd_cursos_presencial,
    ue.ult_ano AS c_ultimo_ano_ead,
    COALESCE(me.qtd_mun_ead, 0) AS d_qtd_mun_ead,
    COALESCE(me.qtd_cursos_ead, 0) AS d_qtd_cursos_ead,
    uu.ult_ano AS e_ultimo_ano_uab,
    COALESCE(pu.qtd_polos_uab, 0) AS f_qtd_polos_uab,
    COALESCE(pu.qtd_cursos_uab, 0) AS f_qtd_cursos_uab,
    COALESCE(m24.tot_mat, 0) AS g_total_matriculas_2024,
    COALESCE(m24.tot_mat_lic, 0) AS h_total_matriculas_lic_2024,
    COALESCE(m24.tot_mat_lic_ead_proprios, 0) AS i_mat_lic_ead_proprios,
    COALESCE(m24.tot_mat_lic_ead_uab, 0) AS j_mat_lic_ead_uab
FROM base b
LEFT JOIN ult_ano_presencial up ON b.ies_codigo = up.ies
LEFT JOIN mun_presencial_ult_ano mp ON b.ies_codigo = mp.ies
LEFT JOIN ult_ano_ead ue ON b.ies_codigo = ue.ies
LEFT JOIN mun_ead_ult_ano me ON b.ies_codigo = me.ies
LEFT JOIN ult_ano_uab uu ON b.ies_codigo = uu.ies
LEFT JOIN polos_uab_ult_ano pu ON b.ies_codigo = pu.ies
LEFT JOIN matriculas_2024 m24 ON b.ies_codigo = m24.ies
ORDER BY 3, 1, 2;

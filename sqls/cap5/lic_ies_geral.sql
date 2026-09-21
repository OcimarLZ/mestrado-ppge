WITH base AS (
    -- Sua consulta original (incluindo o ID da IES para fazer os joins)
    SELECT DISTINCT
        i.codigo AS ies_codigo,
        i.nome AS ies_nome,
        i.sigla,
        i.estado
    FROM ies i
    LEFT JOIN uab_censo uc ON i.codigo = uc.ies 
                           AND uc.tp_grau_academico = 2 
                           AND uc.ano_censo > 2013
    WHERE i.categoria = 1 
      AND i.org_academica = 1
      AND i.nome NOT LIKE 'Universidade codigo%'
),
-- a) Qual o ultimo ano que cada registro de Ies ofertou algum curso de licenciatura presencial
ult_ano_presencial AS (
    SELECT ies, MAX(ano_censo) as ult_ano
    FROM curso_censo
    WHERE tp_grau_academico = 2 AND tp_modalidade_ensino = 1
    GROUP BY ies
),
-- b) A qtde de municipios que a ies esteve neste último ano nesta modalidade
mun_presencial_ult_ano AS (
    SELECT c.ies, COUNT(DISTINCT c.municipio) as qtd_mun_presencial, COUNT(DISTINCT c.curso) as qtd_cursos_presencial
    FROM curso_censo c
    JOIN ult_ano_presencial u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
    WHERE c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 1
    GROUP BY c.ies
),
-- c) Qual o ultimo ano que cada registro de Ies ofertou algum curso de licenciatura EaD
ult_ano_ead AS (
    SELECT ies, MAX(ano_censo) as ult_ano
    FROM curso_censo
    WHERE tp_grau_academico = 2 AND tp_modalidade_ensino = 2
    GROUP BY ies
),
-- d) A qtde de municipios que a ies esteve neste último ano nesta modalidade EaD
mun_ead_ult_ano AS (
    SELECT c.ies, COUNT(DISTINCT c.municipio) as qtd_mun_ead, COUNT(DISTINCT c.curso) as qtd_cursos_ead
    FROM curso_censo c
    JOIN ult_ano_ead u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
    WHERE c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 2
    GROUP BY c.ies
),
-- e) Qual o ultimo ano que cada registro de Ies ofertou algum curso por uab (uab_censo) de licenciatura presencial / ativo
ult_ano_uab AS (
    SELECT ies, MAX(ano_censo) as ult_ano
    FROM uab_censo
    WHERE tp_grau_academico = 2 AND situacao_polo = 'Ativo'
    GROUP BY ies
),
-- f) A qtde de polos c (count de id_polo) que estes cursos foram ofertados no ultimo ano
polos_uab_ult_ano AS (
    SELECT c.ies, COUNT(DISTINCT c.id_polo) as qtd_polos_uab, COUNT(DISTINCT c.nm_curso) as qtd_cursos_uab
    FROM uab_censo c
    JOIN ult_ano_uab u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
    WHERE c.tp_grau_academico = 2 AND c.situacao_polo = 'Ativo'
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
    COALESCE(pu.qtd_cursos_uab, 0) AS f_qtd_cursos_uab
FROM base b
LEFT JOIN ult_ano_presencial up ON b.ies_codigo = up.ies
LEFT JOIN mun_presencial_ult_ano mp ON b.ies_codigo = mp.ies
LEFT JOIN ult_ano_ead ue ON b.ies_codigo = ue.ies
LEFT JOIN mun_ead_ult_ano me ON b.ies_codigo = me.ies
LEFT JOIN ult_ano_uab uu ON b.ies_codigo = uu.ies
LEFT JOIN polos_uab_ult_ano pu ON b.ies_codigo = pu.ies
ORDER BY 3, 1, 2;

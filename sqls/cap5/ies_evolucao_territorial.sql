WITH anos AS (
    SELECT 2014 AS ano_censo UNION SELECT 2015 UNION SELECT 2016 UNION SELECT 2017 UNION SELECT 2018 UNION SELECT 2019 UNION SELECT 2020 UNION SELECT 2021 UNION SELECT 2022 UNION SELECT 2023 UNION SELECT 2024
),
-- 1. Municipios com Campus Ufs (Conta municípios distintos com campi presenciais de UFs)
campus_ufs AS (
    SELECT cc.ano_censo, COUNT(DISTINCT cc.municipio) AS qt
    FROM curso_censo cc
    JOIN ies i ON i.codigo = cc.ies
    WHERE i.categoria = 1 AND i.org_academica = 1
      AND cc.tp_grau_academico = 2
      AND cc.tp_modalidade_ensino = 1
    GROUP BY cc.ano_censo
),
-- 2. Polos EaD Próprios de Ufs (Conta a relação única de IES + Município para polos próprios)
polos_proprios_ufs AS (
    SELECT cc.ano_censo, COUNT(DISTINCT cc.ies || '-' || cc.municipio) AS qt
    FROM curso_censo cc
    JOIN ies i ON i.codigo = cc.ies
    JOIN curso c ON c.codigo = cc.curso
    WHERE i.categoria = 1 AND i.org_academica = 1
      AND cc.tp_grau_academico = 2
      AND cc.tp_modalidade_ensino = 2
      AND c.fl_uab = 'N'
    GROUP BY cc.ano_censo
),
-- 3. Polos UAB de Ufs (Conta a relação única de IES + Município com base no UNION atualizado)
polos_uab_ufs AS (
    SELECT ano_censo, COUNT(DISTINCT ies || '-' || municipio) AS qt
    FROM (
        SELECT u.ano_censo, u.ies, u.municipio
        FROM uab_censo u
        JOIN ies i ON i.codigo = u.ies
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND u.tp_grau_academico = 2
        UNION
        SELECT cc.ano_censo, cc.ies, cc.municipio
        FROM curso_censo cc
        JOIN ies i ON i.codigo = cc.ies
        JOIN curso c ON c.codigo = cc.curso
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND cc.tp_grau_academico = 2
          AND cc.tp_modalidade_ensino = 2
          AND c.fl_uab = 'S'
    ) AS uab_all
    GROUP BY ano_censo
)
SELECT 
    'Municipios com Campus Ufs' AS indicador,
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(c.qt, 0) END) AS "2014",
    MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(c.qt, 0) END) AS "2015",
    MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(c.qt, 0) END) AS "2016",
    MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(c.qt, 0) END) AS "2017",
    MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(c.qt, 0) END) AS "2018",
    MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(c.qt, 0) END) AS "2019",
    MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(c.qt, 0) END) AS "2020",
    MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(c.qt, 0) END) AS "2021",
    MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(c.qt, 0) END) AS "2022",
    MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(c.qt, 0) END) AS "2023",
    MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(c.qt, 0) END) AS "2024"
FROM anos a
LEFT JOIN campus_ufs c ON a.ano_censo = c.ano_censo
UNION ALL
SELECT 
    'Polos EaD Próprios de Ufs',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(p.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(p.qt, 0) END)
FROM anos a
LEFT JOIN polos_proprios_ufs p ON a.ano_censo = p.ano_censo
UNION ALL
SELECT 
    'Polos UAB de Ufs',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(u.qt, 0) END),
    MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(u.qt, 0) END)
FROM anos a
LEFT JOIN polos_uab_ufs u ON a.ano_censo = u.ano_censo;
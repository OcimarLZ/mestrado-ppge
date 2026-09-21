WITH anos AS (
    SELECT 2014 AS ano_censo UNION SELECT 2015 UNION SELECT 2016 UNION SELECT 2017 UNION SELECT 2018 UNION SELECT 2019 UNION SELECT 2020 UNION SELECT 2021 UNION SELECT 2022 UNION SELECT 2023 UNION SELECT 2024
),
-- 1. Municípios com Ufs (Qualquer município que tenha Campus, Polo Próprio ou Polo UAB ligado a uma UF)
municipios_ufs AS (
    SELECT ano_censo, COUNT(DISTINCT municipio) AS qt
    FROM (
        SELECT cc.ano_censo, cc.municipio
        FROM curso_censo cc
        JOIN ies i ON i.codigo = cc.ies
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND cc.tp_grau_academico = 2
        UNION
        SELECT u.ano_censo, u.municipio
        FROM uab_censo u
        JOIN ies i ON i.codigo = u.ies
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND u.tp_grau_academico = 2
    ) AS all_ufs
    GROUP BY ano_censo
),
-- 2. Municipios com Lic.Presencial (Apenas municípios com campi presenciais de UFs)
lic_presencial AS (
    SELECT cc.ano_censo, COUNT(DISTINCT cc.municipio) AS qt
    FROM curso_censo cc
    JOIN ies i ON i.codigo = cc.ies
    WHERE i.categoria = 1 AND i.org_academica = 1
      AND cc.tp_grau_academico = 2
      AND cc.tp_modalidade_ensino = 1
    GROUP BY cc.ano_censo
),
-- 3. Municípios com Polos UAB Geral (Polos UAB somando todas as categorias de IES)
uab_geral AS (
    SELECT ano_censo, COUNT(DISTINCT municipio) AS qt
    FROM (
        SELECT ano_censo, municipio FROM uab_censo WHERE tp_grau_academico = 2
        UNION
        SELECT cc.ano_censo, cc.municipio FROM curso_censo cc
        JOIN curso c ON c.codigo = cc.curso
        WHERE cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'S'
    ) AS uab_all
    GROUP BY ano_censo
),
-- 4. Municipios com Polos UAB nas Ufs (Polos UAB filtrados apenas para UFs)
uab_ufs AS (
    SELECT ano_censo, COUNT(DISTINCT municipio) AS qt
    FROM (
        SELECT u.ano_censo, u.municipio
        FROM uab_censo u
        JOIN ies i ON i.codigo = u.ies
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND u.tp_grau_academico = 2
        UNION
        SELECT cc.ano_censo, cc.municipio
        FROM curso_censo cc
        JOIN ies i ON i.codigo = cc.ies
        JOIN curso c ON c.codigo = cc.curso
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND cc.tp_grau_academico = 2
          AND cc.tp_modalidade_ensino = 2
          AND c.fl_uab = 'S'
    ) AS uab_ufs_all
    GROUP BY ano_censo
),
-- 5. Municípios com Polos UAB outras IES (Polos UAB de todas IES que NÃO são UFs)
uab_outras_ies AS (
    SELECT ano_censo, COUNT(DISTINCT municipio) AS qt
    FROM (
        SELECT u.ano_censo, u.municipio
        FROM uab_censo u
        JOIN ies i ON i.codigo = u.ies
        WHERE NOT (i.categoria = 1 AND i.org_academica = 1)
          AND u.tp_grau_academico = 2
        UNION
        SELECT cc.ano_censo, cc.municipio
        FROM curso_censo cc
        JOIN ies i ON i.codigo = cc.ies
        JOIN curso c ON c.codigo = cc.curso
        WHERE NOT (i.categoria = 1 AND i.org_academica = 1)
          AND cc.tp_grau_academico = 2
          AND cc.tp_modalidade_ensino = 2
          AND c.fl_uab = 'S'
    ) AS uab_outras
    GROUP BY ano_censo
)
SELECT 
    'Municípios com Ufs' AS "Territórios / Modalidade",
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(m.qt, 0) END) AS "2014",
    MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(m.qt, 0) END) AS "2015",
    MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(m.qt, 0) END) AS "2016",
    MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(m.qt, 0) END) AS "2017",
    MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(m.qt, 0) END) AS "2018",
    MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(m.qt, 0) END) AS "2019",
    MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(m.qt, 0) END) AS "2020",
    MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(m.qt, 0) END) AS "2021",
    MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(m.qt, 0) END) AS "2022",
    MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(m.qt, 0) END) AS "2023",
    MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(m.qt, 0) END) AS "2024"
FROM anos a LEFT JOIN municipios_ufs m ON a.ano_censo = m.ano_censo
UNION ALL
SELECT 'Municipios com Lic.Presencial',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(l.qt, 0) END)
FROM anos a LEFT JOIN lic_presencial l ON a.ano_censo = l.ano_censo
UNION ALL
SELECT 'Municpios com Polos UAB Geral',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(g.qt, 0) END)
FROM anos a LEFT JOIN uab_geral g ON a.ano_censo = g.ano_censo
UNION ALL
SELECT 'Municipios com Polos UAB nas Ufs',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(u.qt, 0) END)
FROM anos a LEFT JOIN uab_ufs u ON a.ano_censo = u.ano_censo
UNION ALL
SELECT 'Municípios com Polos UAB outras IES',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(o.qt, 0) END)
FROM anos a LEFT JOIN uab_outras_ies o ON a.ano_censo = o.ano_censo;



WITH presencial AS (
    SELECT
        ano_censo,
        COUNT(DISTINCT municipio) AS qtd_municipios_presencial
    FROM curso_censo
    WHERE ano_censo > 2013 
       and tp_grau_academico = 2
       and categoria = 1
       AND tp_modalidade_ensino = 1
    GROUP BY ano_censo
),
ead_proprio AS (
    SELECT
        ano_censo,
        COUNT(DISTINCT municipio) AS qtd_polos_ead_proprios
    FROM curso_censo
    WHERE ano_censo > 2013 
       and tp_grau_academico = 2
       AND tp_modalidade_ensino = 2
       and categoria = 1
    GROUP BY ano_censo
),
uab AS (
    SELECT
        u.ano_censo,
        COUNT(DISTINCT u.id_polo) AS qtd_polos_uab
    FROM uab_censo u
    JOIN ies i on i.codigo = u.ies
    WHERE u.ano_censo > 2013 
      and u.tp_grau_academico = 2
      and i.categoria = 1
      AND situacao_polo = 'Ativo'
    GROUP BY ano_censo
)
SELECT
    COALESCE(p.ano_censo, e.ano_censo, u.ano_censo) AS ano_censo,
    COALESCE(p.qtd_municipios_presencial, 0) AS qtd_municipios_presencial,
    COALESCE(e.qtd_polos_ead_proprios, 0) AS qtd_polos_ead_proprios,
    COALESCE(u.qtd_polos_uab, 0) AS qtd_polos_uab
FROM presencial p
FULL OUTER JOIN ead_proprio e
    ON p.ano_censo = e.ano_censo
FULL OUTER JOIN uab u
    ON COALESCE(p.ano_censo, e.ano_censo) = u.ano_censo
ORDER BY ano_censo;


WITH anos AS (
    SELECT 2014 AS ano_censo UNION SELECT 2015 UNION SELECT 2016 UNION SELECT 2017 UNION SELECT 2018 UNION SELECT 2019 UNION SELECT 2020 UNION SELECT 2021 UNION SELECT 2022 UNION SELECT 2023 UNION SELECT 2024
),
-- 1. Municípios com Ufs (Qualquer município que tenha Campus, Polo Próprio ou Polo UAB ligado a uma UF)
municipios_ufs AS (
    SELECT ano_censo, COUNT(DISTINCT municipio) AS qt
    FROM (
        SELECT cc.ano_censo, cc.municipio
        FROM curso_censo cc
        JOIN ies i ON i.codigo = cc.ies
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND cc.tp_grau_academico = 2
        UNION
        SELECT u.ano_censo, u.municipio
        FROM uab_censo u
        JOIN ies i ON i.codigo = u.ies
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND u.tp_grau_academico = 2
    ) AS all_ufs
    GROUP BY ano_censo
),
-- 2. Municipios com Lic.Presencial (Apenas municípios com campi presenciais de UFs)
lic_presencial AS (
    SELECT cc.ano_censo, COUNT(DISTINCT cc.municipio) AS qt
    FROM curso_censo cc
    JOIN ies i ON i.codigo = cc.ies
    WHERE i.categoria = 1 AND i.org_academica = 1
      AND cc.tp_grau_academico = 2
      AND cc.tp_modalidade_ensino = 1
    GROUP BY cc.ano_censo
),
-- 3. Municípios com Polos UAB Geral (Polos UAB somando todas as categorias de IES)
uab_geral AS (
    SELECT ano_censo, COUNT(DISTINCT municipio) AS qt
    FROM (
        SELECT ano_censo, municipio FROM uab_censo WHERE tp_grau_academico = 2
        UNION
        SELECT cc.ano_censo, cc.municipio FROM curso_censo cc
        JOIN curso c ON c.codigo = cc.curso
        WHERE cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'S'
    ) AS uab_all
    GROUP BY ano_censo
),
-- 4. Municipios com Polos UAB nas Ufs (Polos UAB filtrados apenas para UFs)
uab_ufs AS (
    SELECT ano_censo, COUNT(DISTINCT municipio) AS qt
    FROM (
        SELECT u.ano_censo, u.municipio
        FROM uab_censo u
        JOIN ies i ON i.codigo = u.ies
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND u.tp_grau_academico = 2
        UNION
        SELECT cc.ano_censo, cc.municipio
        FROM curso_censo cc
        JOIN ies i ON i.codigo = cc.ies
        JOIN curso c ON c.codigo = cc.curso
        WHERE i.categoria = 1 AND i.org_academica = 1
          AND cc.tp_grau_academico = 2
          AND cc.tp_modalidade_ensino = 2
          AND c.fl_uab = 'S'
    ) AS uab_ufs_all
    GROUP BY ano_censo
),
-- 5. Municípios com Polos UAB outras IES (Polos UAB de todas IES que NÃO são UFs)
uab_outras_ies AS (
    SELECT ano_censo, COUNT(DISTINCT municipio) AS qt
    FROM (
        SELECT u.ano_censo, u.municipio
        FROM uab_censo u
        JOIN ies i ON i.codigo = u.ies
        WHERE NOT (i.categoria = 1 AND i.org_academica = 1)
          AND u.tp_grau_academico = 2
        UNION
        SELECT cc.ano_censo, cc.municipio
        FROM curso_censo cc
        JOIN ies i ON i.codigo = cc.ies
        JOIN curso c ON c.codigo = cc.curso
        WHERE NOT (i.categoria = 1 AND i.org_academica = 1)
          AND cc.tp_grau_academico = 2
          AND cc.tp_modalidade_ensino = 2
          AND c.fl_uab = 'S'
    ) AS uab_outras
    GROUP BY ano_censo
)
SELECT 
    'Municípios com Ufs' AS "Territórios / Modalidade",
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(m.qt, 0) END) AS "2014",
    MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(m.qt, 0) END) AS "2015",
    MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(m.qt, 0) END) AS "2016",
    MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(m.qt, 0) END) AS "2017",
    MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(m.qt, 0) END) AS "2018",
    MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(m.qt, 0) END) AS "2019",
    MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(m.qt, 0) END) AS "2020",
    MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(m.qt, 0) END) AS "2021",
    MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(m.qt, 0) END) AS "2022",
    MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(m.qt, 0) END) AS "2023",
    MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(m.qt, 0) END) AS "2024"
FROM anos a LEFT JOIN municipios_ufs m ON a.ano_censo = m.ano_censo
UNION ALL
SELECT 'Municipios com Lic.Presencial',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(l.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(l.qt, 0) END)
FROM anos a LEFT JOIN lic_presencial l ON a.ano_censo = l.ano_censo
UNION ALL
SELECT 'Municpios com Polos UAB Geral',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(g.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(g.qt, 0) END)
FROM anos a LEFT JOIN uab_geral g ON a.ano_censo = g.ano_censo
UNION ALL
SELECT 'Municipios com Polos UAB nas Ufs',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(u.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(u.qt, 0) END)
FROM anos a LEFT JOIN uab_ufs u ON a.ano_censo = u.ano_censo
UNION ALL
SELECT 'Municípios com Polos UAB outras IES',
    MAX(CASE WHEN a.ano_censo = 2014 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2015 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2016 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2017 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2018 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2019 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2020 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2021 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2022 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2023 THEN COALESCE(o.qt, 0) END), MAX(CASE WHEN a.ano_censo = 2024 THEN COALESCE(o.qt, 0) END)
FROM anos a LEFT JOIN uab_outras_ies o ON a.ano_censo = o.ano_censo;


 SELECT cc.ano_censo, 
    COUNT(DISTINCT cc.municipio) AS polos,
    sum(cc.qt_mat) mat
    FROM curso_censo cc
    JOIN curso c ON c.codigo = cc.curso
    WHERE cc.categoria = 1 AND cc.org_academica = 1
      AND cc.tp_grau_academico = 2
      AND cc.tp_modalidade_ensino = 2
      and c.fl_uab = 'N'
      and cc.ano_censo > 2013
    GROUP BY cc.ano_censo
    
SELECT uc.ano_censo, 
    count(Distinct uc.id_polo) polos
    FROM uab_censo uc
    JOIN ies i ON i.codigo = uc.ies
    WHERE i.categoria = 1 
      AND i.org_academica = 1
      AND uc.tp_grau_academico = 2
      and uc.ano_censo > 2013
    GROUP BY 1
    
 SELECT cc.ano_censo, 
    COUNT(DISTINCT cc.municipio) AS polos,
    sum(cc.qt_mat) mat
    FROM curso_censo cc
    WHERE cc.categoria = 1 AND cc.org_academica = 1
      AND cc.tp_grau_academico = 2
      AND cc.tp_modalidade_ensino = 1
      and cc.ano_censo > 2013
    GROUP BY cc.ano_censo

SELECT 
cc.ano_censo, 
sum(cc.qt_mat) mat
    FROM curso_censo cc
    WHERE cc.categoria = 1 AND cc.org_academica = 1
      AND cc.tp_grau_academico = 2
      AND cc.tp_modalidade_ensino = 1
      and cc.ano_censo > 2013
    GROUP BY cc.ano_censo1

  
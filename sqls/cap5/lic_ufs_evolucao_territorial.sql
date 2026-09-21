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
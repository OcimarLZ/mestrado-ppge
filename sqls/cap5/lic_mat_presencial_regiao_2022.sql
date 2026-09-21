WITH matriculas AS (
  SELECT
    r.codigo AS regiao_codigo,
    r.nome   AS regiao,
    SUM(cc.qt_mat) AS matriculas
  FROM curso_censo cc
  JOIN regiao r ON r.codigo = cc.regiao
  WHERE cc.ano_censo = 2022
    AND cc.org_academica = 1
    AND cc.categoria = 1
    AND cc.tp_grau_academico = 2
    AND cc.tp_modalidade_ensino = 1
  GROUP BY r.codigo, r.nome
),
territorio AS (
  SELECT
    r.codigo AS regiao_codigo,
    r.nome   AS regiao,
    SUM(mc.pop_ajustada) AS populacao,
    SUM(mc.area)         AS area_km2
  FROM municipio_censo mc
  JOIN municipio m ON m.codigo = mc.municipio
  JOIN uf u ON u.sigla = m.estado
  JOIN regiao r ON r.codigo = u.regiao
  GROUP BY r.codigo, r.nome
)
SELECT
  coalesce(m.regiao, t.regiao) AS regiao,
  coalesce(m.matriculas, 0)    AS matriculas_presenciais,
  coalesce(t.populacao, 0)     AS populacao,
  -- Matrículas por 100.000 habitantes
  CASE WHEN coalesce(t.populacao,0) = 0 THEN NULL
       ELSE round( (coalesce(m.matriculas,0) * 100000.0) / t.populacao, 2)
  END AS matriculas_por_100k_hab,
  coalesce(t.area_km2, 0)      AS area_km2,
  -- Matrículas por 1.000 km²
  CASE WHEN coalesce(t.area_km2,0) = 0 THEN NULL
       ELSE round( (coalesce(m.matriculas,0) * 1000.0) / t.area_km2, 2)
  END AS matriculas_por_1000_km2
FROM matriculas m
FULL OUTER JOIN territorio t
  ON m.regiao_codigo = t.regiao_codigo
ORDER BY regiao;
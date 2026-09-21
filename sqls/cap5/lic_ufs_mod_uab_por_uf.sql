
-- Cálculo de percentual de matrículas de licenciaturas em universidades federais
-- por modalidade (Presencial, EaD Próprio, EaD UAB) e por UF
-- Anos 2014-2024
SELECT
    cc.ano_censo,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_mat ELSE 0 END) AS mat_presencial,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'N' THEN cc.qt_mat ELSE 0 END) AS mat_ead_proprio,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'S' THEN cc.qt_mat ELSE 0 END) AS mat_ead_uab,
    SUM(cc.qt_mat) AS mat_total,
    ROUND(
        (SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_mat ELSE 0 END) * 100.0) / NULLIF(SUM(cc.qt_mat), 0),
        2
    ) AS pct_presencial,
    ROUND(
        (SUM(CASE WHEN cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'N' THEN cc.qt_mat ELSE 0 END) * 100.0) / NULLIF(SUM(cc.qt_mat), 0),
        2
    ) AS pct_ead_proprio,
    ROUND(
        (SUM(CASE WHEN cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'S' THEN cc.qt_mat ELSE 0 END) * 100.0) / NULLIF(SUM(cc.qt_mat), 0),
        2
    ) AS pct_ead_uab
FROM curso_censo cc
JOIN curso c ON c.codigo = cc.curso
WHERE cc.ano_censo > 2013
  AND cc.tp_grau_academico = 2
  AND cc.org_academica = 1
  AND cc.categoria = 1
GROUP BY cc.ano_censo
ORDER BY cc.ano_censo

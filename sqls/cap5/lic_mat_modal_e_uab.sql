SELECT
    cc.ano_censo,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_mat ELSE 0 END) AS mat_presencial,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'N' THEN cc.qt_mat ELSE 0 END) AS mat_ead_proprio,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'S' THEN cc.qt_mat ELSE 0 END) AS mat_ead_uab
FROM curso_censo cc
JOIN curso c ON c.codigo = cc.curso
WHERE cc.ano_censo > 2013
  AND cc.tp_grau_academico = 2
  AND cc.org_academica = 1
  AND cc.categoria = 1
GROUP BY cc.ano_censo
ORDER BY cc.ano_censo
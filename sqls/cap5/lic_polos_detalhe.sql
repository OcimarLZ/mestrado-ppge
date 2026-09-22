-- Detalhamento por campus/polo das licenciaturas das IES publicas federais (UFs), 2014 e
-- 2024: uma linha por IES x ano x municipio x tipo de oferta (Presencial / EaD proprio /
-- UAB), com o numero de cursos e o total de matriculas (qt_mat) naquele polo.
--
-- Complementa sqls/cap5/lic_ies_geral.sql (que traz totais por IES) descendo ao nivel de
-- cada campus/polo -- e a base de dados de web_app/content_export/export_lic_polos_detalhe.py.
SELECT
    i.nome AS ies_nome,
    i.sigla,
    i.estado AS ies_uf,
    cc.ano_censo,
    m.nome AS municipio,
    m.uf AS municipio_uf,
    CASE
        WHEN cc.tp_modalidade_ensino = 1 THEN 'Presencial'
        WHEN c.fl_uab = 'S' THEN 'UAB'
        ELSE 'EaD próprio'
    END AS tipo_polo,
    COUNT(DISTINCT cc.curso) AS num_cursos,
    SUM(cc.qt_mat) AS matriculas
FROM superior_curso_censo cc
JOIN superior_curso c ON c.codigo = cc.curso
JOIN superior_ies i ON i.codigo = cc.ies
JOIN comum_municipio m ON m.codigo = cc.municipio
WHERE cc.ano_censo IN (2014, 2024)
  AND cc.tp_grau_academico = 2
  AND i.categoria = 1
  AND i.org_academica = 1
  AND i.nome NOT LIKE 'Universidade codigo%'
GROUP BY i.codigo, cc.ano_censo, cc.municipio, tipo_polo
ORDER BY i.estado, i.nome, cc.ano_censo, matriculas DESC;

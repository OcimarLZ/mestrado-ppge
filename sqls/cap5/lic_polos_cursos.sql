-- Detalhamento por curso dentro de cada campus/polo das licenciaturas das IES publicas
-- federais (UFs), 2014 e 2024: uma linha por IES x ano x municipio x tipo de polo
-- (Presencial / EaD proprio / UAB) x curso, com o total de matriculas (qt_mat) daquele
-- curso naquele polo.
--
-- Mesma classificacao de tipo_polo de sqls/cap5/lic_polos_detalhe.sql (que agrega so ate o
-- nivel de polo); esta consulta desce mais um nivel, ate o curso -- e a base de dados de
-- web_app/content_export/export_lic_polos_cursos.py, usada para expandir cada linha da
-- tabela de polos e mostrar os cursos ali ofertados.
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
    c.nome AS curso,
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
GROUP BY i.codigo, cc.ano_censo, cc.municipio, tipo_polo, c.codigo
ORDER BY i.estado, i.nome, cc.ano_censo, matriculas DESC;

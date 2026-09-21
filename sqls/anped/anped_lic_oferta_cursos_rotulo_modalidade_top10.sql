WITH base AS (
	SELECT
		cc.ano_censo,
		cc.curso,
		cc.cine_rotulo,
		COALESCE(cr.nome, cc.cine_rotulo) AS cine_rotulo_descricao,
		CASE
			WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
			ELSE 'presencial'
		END AS modalidade
	FROM curso_censo cc
	LEFT JOIN cine_rotulo cr ON cr.codigo = cc.cine_rotulo
	WHERE cc.ano_censo > 2013
	  AND cc.tp_grau_academico = 2
),
totais AS (
	SELECT
		b.cine_rotulo,
		b.cine_rotulo_descricao,
		COUNT(DISTINCT b.curso) AS qtd_cursos_periodo
	FROM base b
	GROUP BY b.cine_rotulo, b.cine_rotulo_descricao
),
top10 AS (
	SELECT
		t.cine_rotulo,
		t.cine_rotulo_descricao,
		t.qtd_cursos_periodo
	FROM totais t
	ORDER BY t.qtd_cursos_periodo DESC, t.cine_rotulo DESC
	LIMIT 10
),
ofertas_ano AS (
	SELECT
		b.ano_censo,
		b.cine_rotulo,
		b.cine_rotulo_descricao,
		b.modalidade,
		COUNT(DISTINCT b.curso) AS qtd_cursos_ano
	FROM base b
	GROUP BY b.ano_censo, b.cine_rotulo, b.cine_rotulo_descricao, b.modalidade
)
SELECT
	oa.ano_censo,
	oa.cine_rotulo,
	oa.cine_rotulo_descricao,
	oa.modalidade,
	oa.qtd_cursos_ano
FROM ofertas_ano oa
JOIN top10 t ON t.cine_rotulo = oa.cine_rotulo
ORDER BY oa.ano_censo, oa.qtd_cursos_ano DESC, oa.cine_rotulo DESC, oa.modalidade;

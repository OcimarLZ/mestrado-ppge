SELECT 
cc.ano_censo,
r.nome as regiao,
COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.curso ELSE NULL END) AS "Cursos Presenciais",
COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'N' THEN cc.curso ELSE NULL END) AS "Cursos EaD Próprio",
COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'S' THEN cc.curso ELSE NULL END) AS "Cursos UAB"
from curso_censo cc
join curso c on c.codigo = cc.curso
join regiao r on r.codigo = cc.regiao 
where cc.tp_grau_academico = 2 and cc.ano_censo > 2013 and cc.categoria = 1 and cc.org_academica = 1
group by 1,2
SELECT 
cc.ano_censo,
r.nome as regiao,
COUNT(DISTINCT cc.curso) AS qtd_cursos_federais
from curso_censo cc
join regiao r on r.codigo = cc.regiao 
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2 and cc.org_academica = 1 and cc.categoria = 1 and cc.tp_modalidade_ensino = 2
group by 1,2
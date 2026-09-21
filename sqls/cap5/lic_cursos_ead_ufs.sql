SELECT 
cc.ano_censo,
COUNT(DISTINCT cc.curso) AS qtd_cursos_ead_federais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2 and cc.org_academica = 1 and cc.tp_modalidade_ensino = 2 and cc.categoria = 1
group by 1
SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_federais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2 and cc.org_academica = 1
group by 1
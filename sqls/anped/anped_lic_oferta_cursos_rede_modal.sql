SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_publicas,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_privadas
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1
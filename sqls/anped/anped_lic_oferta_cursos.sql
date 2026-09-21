SELECT 
cc.ano_censo,
count(distinct cc.curso) qtd_cursos
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1
SELECT 
cc.ano_censo,
ad.nome as area_detalhada,
COUNT(DISTINCT cc.curso) AS qtd_cursos
from curso_censo cc
join area_detalhada ad on ad.codigo = cc.area_detalhada  
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2
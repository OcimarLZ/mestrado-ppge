SELECT 
cc.ano_censo,
tga.nome as grau_academico,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_publicas,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_privadas
from curso_censo cc
join tp_grau_academico tga on tga.codigo = cc.tp_grau_academico 
where cc.ano_censo > 2013
group by 1,2
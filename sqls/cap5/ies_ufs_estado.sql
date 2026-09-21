SELECT 
cc.ano_censo,
u.nome as estado,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_federais
from curso_censo cc
join uf u on u.sigla = cc.estado 
where cc.ano_censo > 2013 and cc.org_academica = 1 and cc.categoria = 1  and cc.tp_modalidade_ensino = 1
group by 1,2
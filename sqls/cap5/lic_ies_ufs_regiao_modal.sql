SELECT 
cc.ano_censo,
r.nome as regiao,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_federais
from curso_censo cc
join regiao r on r.codigo = cc.regiao 
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2 and cc.org_academica = 1
group by 1,2,3
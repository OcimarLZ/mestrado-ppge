SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.org_academica = 1 THEN cc.ies ELSE NULL END) AS qtd_univ_privadas,
COUNT(DISTINCT CASE WHEN cc.org_academica = 2 THEN cc.ies ELSE NULL END) AS qtd_centros_privadas,
COUNT(DISTINCT CASE WHEN cc.org_academica = 3 THEN cc.ies ELSE NULL END) AS qtd_faculd_privadas
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2 and cc.categoria in (4,5,6,8,9) 
group by 1
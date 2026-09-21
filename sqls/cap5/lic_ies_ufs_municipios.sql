SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 1 THEN cc.municipio ELSE NULL END) AS qtd_municipios
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2 and cc.org_academica = 1 and cc.categoria = 1
group by 1
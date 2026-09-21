SELECT
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_publicas,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_privadas
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2
SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.org_academica = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_universidades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_centro,
COUNT(DISTINCT CASE WHEN cc.org_academica = 3 THEN cc.ies ELSE NULL END) AS qtd_ies_faculdades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 4 THEN cc.ies ELSE NULL END) AS qtd_ies_institutos,
COUNT(DISTINCT CASE WHEN cc.org_academica = 5 THEN cc.ies ELSE NULL END) AS qtd_ies_cefet
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2
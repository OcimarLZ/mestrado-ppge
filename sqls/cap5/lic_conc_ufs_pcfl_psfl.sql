SELECT 
cc.ano_censo,
SUM(CASE WHEN cc.categoria = 1 and cc.org_academica = 1 THEN cc.qt_conc ELSE NULL END) AS conc_ufs,
SUM(CASE WHEN cc.categoria in (4,6) THEN cc.qt_conc ELSE NULL END) AS conc_privadas_cfl,
SUM(CASE WHEN cc.categoria in (5,7,8) THEN cc.qt_conc ELSE NULL END) AS conc_privadas_sfl
from curso_censo cc
join curso c on c.codigo = cc.curso
where cc.tp_grau_academico = 2 and cc.ano_censo > 2013 
group by 1
order by 1
SELECT 
cc.ano_censo,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and cc.org_academica = 1 and cc.categoria = 1 THEN cc.qt_ing ELSE NULL END) AS ingressos_ead_ufs,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and cc.categoria in (4,6) THEN cc.qt_ing ELSE NULL END) AS ingressos_pcls,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and cc.categoria in (5,7,8) THEN cc.qt_ing ELSE NULL END) AS ingressos_psls
from curso_censo cc
join curso c on c.codigo = cc.curso
where cc.tp_grau_academico = 2 and cc.ano_censo > 2013
group by 1
order by 1
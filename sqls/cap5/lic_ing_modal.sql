SELECT DISTINCT 
cc.ano_censo,
SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_ing ELSE NULL END) AS "Ingressos Presencial",
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'N' THEN cc.qt_ing ELSE NULL END) AS "Ingressos EaD Próprio",
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'S' THEN cc.qt_ing ELSE NULL END) AS "Ingressos UAB"
from curso_censo cc
join curso c on c.codigo = cc.curso
where cc.tp_grau_academico = 2 and cc.ano_censo > 2013 and cc.categoria = 1 and cc.org_academica = 1
group by 1
order by 1
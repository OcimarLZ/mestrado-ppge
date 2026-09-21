SELECT DISTINCT 
cc.ano_censo,
SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_sit_desvinculado ELSE NULL END) AS evadidos_pres,
SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_sit_trancada ELSE NULL END) AS trancados_pres,
SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_sit_transferido ELSE NULL END) AS transferidos_pres,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'S' THEN cc.qt_sit_desvinculado ELSE NULL END) AS evadidos_uab,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'S' THEN cc.qt_sit_trancada ELSE NULL END) AS trancados_uab,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'S' THEN cc.qt_sit_transferido ELSE NULL END) AS transferidos_uab,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'N' THEN cc.qt_sit_desvinculado ELSE NULL END) AS evadidos_ead,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'N' THEN cc.qt_sit_trancada ELSE NULL END) AS trancados_ead,
SUM(CASE WHEN cc.tp_modalidade_ensino = 2 and c.fl_uab = 'N' THEN cc.qt_sit_transferido ELSE NULL END) AS transferidos_ead
from curso_censo cc
join curso c on c.codigo = cc.curso
where cc.tp_grau_academico = 2 and cc.ano_censo > 2013 and cc.categoria = 1 and cc.org_academica = 1
group by 1
order by 1
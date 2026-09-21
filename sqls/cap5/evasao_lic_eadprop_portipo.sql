SELECT 
cc.ano_censo,
SUM(cc.qt_sit_desvinculado) AS Desvinculados,
SUM(cc.qt_sit_trancada) AS Trancados,
SUM(cc.qt_sit_transferido) AS Tranferidos
from curso_censo cc
join curso c on c.codigo = cc.curso
where cc.tp_grau_academico = 2 and cc.ano_censo > 2013 and cc.categoria = 1 and cc.org_academica = 1 and cc.tp_modalidade_ensino = 2 and c.fl_uab = 'N'
group by 1
order by 1
SELECT distinct
cc.ano_censo,
sum(cc.qt_mat) matriculas
from curso_censo cc
join ies i on i.codigo = cc.ies 
where cc.ano_censo > 2013 and cc.org_academica = 1 and cc.categoria = 1 and cc.tp_grau_academico = 2 and cc.tp_modalidade_ensino = 1
group by 1
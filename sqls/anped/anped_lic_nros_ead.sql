SELECT 
cc.ano_censo,
sum(cc.qt_vg_total) vagas,
sum(qt_inscrito_total) inscritos,
sum(cc.qt_ing) ingressos,
sum(cc.qt_mat) matriculados,
sum(cc.qt_conc) concluintes,
sum(cc.qt_sit_desvinculado + cc.qt_sit_transferido) evadidos,
sum(cc.qt_sit_trancada) trancados
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2 and cc.tp_modalidade_ensino = 2
group by 1
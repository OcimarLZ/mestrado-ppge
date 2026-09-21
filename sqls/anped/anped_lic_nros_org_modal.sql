SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
CASE 
   WHEN cc.org_academica = 1 THEN 'Universidade'
   WHEN cc.org_academica = 2 THEN 'Centro'
   WHEN cc.org_academica = 3 THEN 'Faculdade'
   WHEN cc.org_academica = 4 THEN 'Instituto'
   WHEN cc.org_academica = 5 THEN 'CEFET'
   ELSE 'Outras'
END AS tipoorg,
sum(cc.qt_vg_total) vagas,
sum(qt_inscrito_total) inscritos,
sum(cc.qt_ing) ingressos,
sum(cc.qt_mat) matriculados,
sum(cc.qt_conc) concluintes,
sum(cc.qt_sit_desvinculado + cc.qt_sit_transferido) evadidos,
sum(cc.qt_sit_trancada) trancados
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2,3
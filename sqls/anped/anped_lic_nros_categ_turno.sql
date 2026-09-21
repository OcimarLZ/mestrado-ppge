SELECT 
cc.ano_censo,
CASE 
   WHEN cc.categoria = 1 THEN 'Federal'
   WHEN cc.categoria = 2 THEN 'Estadual'
   WHEN cc.categoria = 3 THEN 'Municipal'
   WHEN cc.categoria = 4 THEN 'Privada CFins Lucro'
   WHEN cc.categoria = 5 THEN 'Privada SFins Lucro'
   WHEN cc.categoria = 7 THEN 'Especial'
   ELSE 'Outras'
END AS categoria,
sum(cc.qt_vg_total_diurno) vagas_diurno, 
sum(cc.qt_vg_total_noturno) vagas_noturno,
sum(cc.qt_vg_total_ead) vagas_ead,
sum(cc.qt_inscrito_total_diurno) inscritos_diurno,
sum(cc.qt_inscrito_total_noturno) inscritos_noturno,
sum(cc.qt_inscrito_total_ead) inscritos_ead,
sum(cc.qt_ing_diurno) ingressos_diruno,
sum(cc.qt_ing_noturno) ingressos_noturno,
sum(cc.qt_mat_diurno) matriculados_diurno,
sum(cc.qt_mat_noturno) matriculados_noturno,
sum(cc.qt_conc_diurno) concluintes_diurno,
sum(cc.qt_conc_noturno) concluintes_noturno,
sum(cc.qt_sit_desvinculado + cc.qt_sit_transferido) evadidos,
sum(cc.qt_sit_trancada) trancados
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2
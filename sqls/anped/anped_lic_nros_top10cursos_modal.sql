SELECT 
cc.ano_censo,
cr.nome as cine_rotulo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
sum(cc.qt_ing) Ingressos,
sum(cc.qt_mat) Matriculas,
sum(cc.qt_conc) Concluites,
sum(cc.qt_sit_trancada) Trancados,
sum(cc.qt_sit_desvinculado + cc.qt_sit_transferido) Evadidos
from curso_censo cc
join cine_rotulo cr on cr.codigo = cc.cine_rotulo 
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2 and cc.cine_rotulo in ('0113E02', '0113P01', '0114A02', '0114B01', '0114C03', '0114E03', '0114G01', '0114H01', '0114M01', '0115L13')
group by 1,2,3
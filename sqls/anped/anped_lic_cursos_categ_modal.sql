SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.curso ELSE NULL END) AS qtd_cursos_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria in (4,6) THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria in (5,8,9) THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.curso ELSE NULL END) AS qtd_cursos_especiais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2
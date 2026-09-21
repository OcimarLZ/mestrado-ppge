 SELECT 
cc.ano_censo,
tga.nome as grau_academico,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.curso ELSE NULL END) AS qtd_cursos_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria in (4,6) THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria in (5,8,9) THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.curso ELSE NULL END) AS qtd_cursos_especiais
from curso_censo cc
join tp_grau_academico tga on tga.codigo = cc.tp_grau_academico
where cc.ano_censo > 2013
group by 1,2
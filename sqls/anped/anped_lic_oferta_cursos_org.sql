SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.org_academica = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_universidades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_centro,
COUNT(DISTINCT CASE WHEN cc.org_academica = 3 THEN cc.curso ELSE NULL END) AS qtd_cursos_faculdades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 4 THEN cc.curso ELSE NULL END) AS qtd_cursos_institutos,
COUNT(DISTINCT CASE WHEN cc.org_academica = 5 THEN cc.curso ELSE NULL END) AS qtd_cursos_cefet
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1
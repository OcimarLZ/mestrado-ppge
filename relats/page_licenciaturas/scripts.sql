SELECT 
cc.ano_censo,
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Licenciaturas geral
# Qtde de IES que ofertam Licenciaturas (Geral)

SELECT 
cc.ano_censo,
count(distinct cc.ies) qtd_ies
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Qtde de IES que ofertam Licenciaturas por rede

SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_publicas,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_privadas
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Qtde de IES que ofertam Licenciaturas por categoria administrativa

SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.ies ELSE NULL END) AS qtd_ies_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria in (4,6) THEN cc.ies ELSE NULL END) AS qtd_ies_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria in (5,8,9) THEN cc.ies ELSE NULL END) AS qtd_ies_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.ies ELSE NULL END) AS qtd_ies_especiais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.ies ELSE NULL END) AS qtd_ies_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria = 4 THEN cc.ies ELSE NULL END) AS qtd_ies_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 5 THEN cc.ies ELSE NULL END) AS qtd_ies_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 6 THEN cc.ies ELSE NULL END) AS qtd_ies_priv_particulares,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.ies ELSE NULL END) AS qtd_ies_especiais,
COUNT(DISTINCT CASE WHEN cc.categoria = 8 THEN cc.ies ELSE NULL END) AS qtd_ies_comunitarias,
COUNT(DISTINCT CASE WHEN cc.categoria = 9 THEN cc.ies ELSE NULL END) AS qtd_ies_confessionais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Qtde de IES que ofertam Licenciaturas por organização academica

SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.org_academica = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_universidades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_centro,
COUNT(DISTINCT CASE WHEN cc.org_academica = 3 THEN cc.ies ELSE NULL END) AS qtd_ies_faculdades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 4 THEN cc.ies ELSE NULL END) AS qtd_ies_institutos,
COUNT(DISTINCT CASE WHEN cc.org_academica = 5 THEN cc.ies ELSE NULL END) AS qtd_ies_cefet
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Por modalidade
# Qtde de IES que ofertam Licenciaturas (Geral)

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
count(distinct cc.ies) qtd_ies
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Qtde de IES que ofertam Licenciaturas por rede

SELECT
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_publicas,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_privadas
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Qtde de IES que ofertam Licenciaturas por categoria administrativa

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.ies ELSE NULL END) AS qtd_ies_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria in (4,6) THEN cc.ies ELSE NULL END) AS qtd_ies_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria in (5,8,9) THEN cc.ies ELSE NULL END) AS qtd_ies_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.ies ELSE NULL END) AS qtd_ies_especiais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.ies ELSE NULL END) AS qtd_ies_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria = 4 THEN cc.ies ELSE NULL END) AS qtd_ies_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 5 THEN cc.ies ELSE NULL END) AS qtd_ies_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 6 THEN cc.ies ELSE NULL END) AS qtd_ies_priv_particulares,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.ies ELSE NULL END) AS qtd_ies_especiais,
COUNT(DISTINCT CASE WHEN cc.categoria = 8 THEN cc.ies ELSE NULL END) AS qtd_ies_comunitarias,
COUNT(DISTINCT CASE WHEN cc.categoria = 9 THEN cc.ies ELSE NULL END) AS qtd_ies_confessionais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2


# Qtde de IES que ofertam Licenciaturas por organização academica

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.org_academica = 1 THEN cc.ies ELSE NULL END) AS qtd_ies_universidades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 2 THEN cc.ies ELSE NULL END) AS qtd_ies_centro,
COUNT(DISTINCT CASE WHEN cc.org_academica = 3 THEN cc.ies ELSE NULL END) AS qtd_ies_faculdades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 4 THEN cc.ies ELSE NULL END) AS qtd_ies_institutos,
COUNT(DISTINCT CASE WHEN cc.org_academica = 5 THEN cc.ies ELSE NULL END) AS qtd_ies_cefet
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Cursos
# Qtde de cursos geral

SELECT 
cc.ano_censo,
count(distinct cc.curso) qtd_cursos
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Qtde de cursos de Licenciaturas por rede

SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_publicas,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_privadas
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Qtde de cursos de Licenciaturas por categoria administrativa

SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.curso ELSE NULL END) AS qtd_cursos_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria in (4,6) THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria in (5,8,9) THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.curso ELSE NULL END) AS qtd_cursos_especiais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.curso ELSE NULL END) AS qtd_cursos_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria = 4 THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 5 THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 6 THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_particulares,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.curso ELSE NULL END) AS qtd_cursos_especiais,
COUNT(DISTINCT CASE WHEN cc.categoria = 8 THEN cc.curso ELSE NULL END) AS qtd_cursos_comunitarias,
COUNT(DISTINCT CASE WHEN cc.categoria = 9 THEN cc.curso ELSE NULL END) AS qtd_cursos_confessionais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1


# Qtde de cursos em Licenciaturas por organização academica

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

# Crusos de licenciatura por área

SELECT 
cc.ano_censo,
COUNT(DISTINCT CASE WHEN cc.area_geral = 0 THEN cc.curso ELSE NULL END) AS qtd_cursos_progbasico,
COUNT(DISTINCT CASE WHEN cc.area_geral = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_educacao,
COUNT(DISTINCT CASE WHEN cc.area_geral = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_artes,
COUNT(DISTINCT CASE WHEN cc.area_geral = 3 THEN cc.curso ELSE NULL END) AS qtd_cursos_cienciassociais,
COUNT(DISTINCT CASE WHEN cc.area_geral = 4 THEN cc.curso ELSE NULL END) AS qtd_cursos_negocios,
COUNT(DISTINCT CASE WHEN cc.area_geral = 5 THEN cc.curso ELSE NULL END) AS qtd_cursos_cienciasnaturais,
COUNT(DISTINCT CASE WHEN cc.area_geral = 6 THEN cc.curso ELSE NULL END) AS qtd_cursos_tecnologias,
COUNT(DISTINCT CASE WHEN cc.area_geral = 7 THEN cc.curso ELSE NULL END) AS qtd_cursos_engenharias,
COUNT(DISTINCT CASE WHEN cc.area_geral = 8 THEN cc.curso ELSE NULL END) AS qtd_cursos_agricultura,
COUNT(DISTINCT CASE WHEN cc.area_geral = 9 THEN cc.curso ELSE NULL END) AS qtd_cursos_saude,
COUNT(DISTINCT CASE WHEN cc.area_geral = 10 THEN cc.curso ELSE NULL END) AS qtd_cursos_servicos
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Cursos de licenciatura por área específica

SELECT 
cc.ano_censo,
ae.nome as areaespecifica,
COUNT(DISTINCT cc.curso) AS qtd_cursos_areaesp
from curso_censo cc
join area_especifica ae on ae.codigo = cc.area_especifica 
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Cursos de licenciatura por área detalhada

SELECT 
cc.ano_censo,
ad.nome as areadetalhada,
COUNT(DISTINCT cc.curso) AS qtd_cursos_areadet
from curso_censo cc
join area_detalhada ad on ad.codigo = cc.area_detalhada  
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Cursos de licenciatura por rótulo

SELECT 
cc.ano_censo,
cr.nome as rotula,
COUNT(DISTINCT cc.curso) AS qtd_cursos_areadet
from curso_censo cc
join cine_rotulo cr on cr.codigo = cc.cine_rotulo   
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Cursos de licenciatura nome do curso

SELECT 
cc.ano_censo,
UPPER(c.nome)_nomecurso,
COUNT(DISTINCT cc.curso) AS qtd_cursos
from curso_censo cc
join curso c on c.codigo = cc.curso   
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2


# Por modalidade
# Qtde de cursos em licenciatura por modalidade de ensino (Geral)

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
count(distinct cc.curso) qtd_cursos
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Qtde de IES que ofertam Licenciaturas por rede

SELECT
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_publicas,
COUNT(DISTINCT CASE WHEN cc.tp_rede = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_privadas
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Qtde de IES que ofertam Licenciaturas por categoria administrativa

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

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.categoria = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_federais,
COUNT(DISTINCT CASE WHEN cc.categoria = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_estaduais,
COUNT(DISTINCT CASE WHEN cc.categoria = 3 THEN cc.curso ELSE NULL END) AS qtd_cursos_municipais,
COUNT(DISTINCT CASE WHEN cc.categoria = 4 THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_cflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 5 THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_sflucro,
COUNT(DISTINCT CASE WHEN cc.categoria = 6 THEN cc.curso ELSE NULL END) AS qtd_cursos_priv_particulares,
COUNT(DISTINCT CASE WHEN cc.categoria = 7 THEN cc.curso ELSE NULL END) AS qtd_cursos_especiais,
COUNT(DISTINCT CASE WHEN cc.categoria = 8 THEN cc.curso ELSE NULL END) AS qtd_cursos_comunitarias,
COUNT(DISTINCT CASE WHEN cc.categoria = 9 THEN cc.curso ELSE NULL END) AS qtd_cursos_confessionais
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2


# Qtde de cursos em Licenciaturas por organização academica

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
COUNT(DISTINCT CASE WHEN cc.org_academica = 1 THEN cc.curso ELSE NULL END) AS qtd_cursos_universidades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 2 THEN cc.curso ELSE NULL END) AS qtd_cursos_centro,
COUNT(DISTINCT CASE WHEN cc.org_academica = 3 THEN cc.curso ELSE NULL END) AS qtd_cursos_faculdades,
COUNT(DISTINCT CASE WHEN cc.org_academica = 4 THEN cc.curso ELSE NULL END) AS qtd_cursos_institutos,
COUNT(DISTINCT CASE WHEN cc.org_academica = 5 THEN cc.curso ELSE NULL END) AS qtd_cursos_cefet
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Vagas, inscritos, ingressos, matriculados, concluidos, evadidos, trancados
# Geral

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
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1

# Numeros das Licenciaturas por rede

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_rede = 1 THEN 'Publica'
   ELSE 'Privada'
END AS rede,
sum(cc.qt_vg_total) vagas,
sum(qt_inscrito_total) inscritos,
sum(cc.qt_ing) ingressos,
sum(cc.qt_mat) matriculados,
sum(cc.qt_conc) concluintes,
sum(cc.qt_sit_desvinculado + cc.qt_sit_transferido) evadidos,
sum(cc.qt_sit_trancada) trancados
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Numeros das Licenciaturas por categoria administrativa

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
END AS rede,
sum(cc.qt_vg_total) vagas,
sum(qt_inscrito_total) inscritos,
sum(cc.qt_ing) ingressos,
sum(cc.qt_mat) matriculados,
sum(cc.qt_conc) concluintes,
sum(cc.qt_sit_desvinculado + cc.qt_sit_transferido) evadidos,
sum(cc.qt_sit_trancada) trancados
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Numeros das Licenciaturas por organização academica

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.org_academica = 1 THEN 'Universidade'
   WHEN cc.org_academica = 2 THEN 'Centro'
   WHEN cc.org_academica = 3 THEN 'Faculdade'
   WHEN cc.org_academica = 4 THEN 'Instituto'
   WHEN cc.org_academica = 5 THEN 'CEFET'
   ELSE 'Outras'
END AS rede,
sum(cc.qt_vg_total) vagas,
sum(qt_inscrito_total) inscritos,
sum(cc.qt_ing) ingressos,
sum(cc.qt_mat) matriculados,
sum(cc.qt_conc) concluintes,
sum(cc.qt_sit_desvinculado + cc.qt_sit_transferido) evadidos,
sum(cc.qt_sit_trancada) trancados
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Geral
# Geral por modalidade de ensino

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
sum(cc.qt_vg_total) vagas,
sum(qt_inscrito_total) inscritos,
sum(cc.qt_ing) ingressos,
sum(cc.qt_mat) matriculados,
sum(cc.qt_conc) concluintes,
sum(cc.qt_sit_desvinculado + cc.qt_sit_transferido) evadidos,
sum(cc.qt_sit_trancada) trancados
from curso_censo cc
where cc.ano_censo > 2013 and cc.tp_grau_academico = 2
group by 1,2

# Numeros das Licenciaturas por rede e modalidade de ensino

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
CASE 
   WHEN cc.tp_rede = 1 THEN 'Publica'
   ELSE 'Privada'
END AS rede,
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

# Numeros das Licenciaturas por categoria administrativa e modalidade de ensino

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.tp_modalidade_ensino = 2 THEN 'ead'
   ELSE 'presencial'
END AS modalidade,
CASE 
   WHEN cc.categoria = 1 THEN 'Federal'
   WHEN cc.categoria = 2 THEN 'Estadual'
   WHEN cc.categoria = 3 THEN 'Municipal'
   WHEN cc.categoria = 4 THEN 'Privada CFins Lucro'
   WHEN cc.categoria = 5 THEN 'Privada SFins Lucro'
   WHEN cc.categoria = 7 THEN 'Especial'
   ELSE 'Outras'
END AS categoria,
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

# Numeros das Licenciaturas por organização academica

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

# Numeros das Licenciaturas por organização academica

SELECT 
cc.ano_censo,
CASE 
   WHEN cc.org_academica = 1 THEN 'Universidade'
   WHEN cc.org_academica = 2 THEN 'Centro'
   WHEN cc.org_academica = 3 THEN 'Faculdade'
   WHEN cc.org_academica = 4 THEN 'Instituto'
   WHEN cc.org_academica = 5 THEN 'CEFET'
   ELSE 'Outras'
END AS rede,
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

# Numeros das Licenciaturas por categoria administrativa

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


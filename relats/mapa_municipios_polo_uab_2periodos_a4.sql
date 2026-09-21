SELECT DISTINCT 
u.ano_censo,
u.municipio
from uab_censo u
where u.ano_censo in (2014, 2024) and u.tp_grau_academico = 2 and u.situacao_polo = 'Ativo'
ORDER by 1

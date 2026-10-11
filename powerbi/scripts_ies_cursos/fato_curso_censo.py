# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
fato_curso_censo. Cada tabela do modelo tem seu proprio script (ver README.md na pasta
powerbi/) porque o conector Python do Power BI reavalia a arvore de dependencias inteira
do script a cada tabela carregada -- um unico script com 12 variaveis fazia a fato de
~3,9M linhas ser relida/reprocessada uma vez por tabela, esgotando a memoria disponivel
(ArrayMemoryError) mesmo para as dimensoes pequenas.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"
ANO_MIN = 2005
ANO_MAX = 2024

con = sqlite3.connect(DB_PATH)

# Grao: uma linha por curso-oferta x IES x ano_censo. Mantem o codigo de `curso` (a
# oferta especifica, com nome dado pela propria instituicao) ALEM do cine_rotulo (tipo
# padronizado) -- os dois sao necessarios: para contar "quantos cursos distintos" por
# IES usa-se `curso`; para comparar por "tipo de curso" entre IES/anos usa-se cine_rotulo.
fato_curso_censo = pd.read_sql_query(
    f"""
    SELECT
        ano_censo                          AS codigo_ano,
        CAST(municipio AS INTEGER)         AS codigo_municipio,
        ies                                 AS codigo_ies,
        curso                               AS codigo_curso,
        cine_rotulo                         AS codigo_cine_rotulo,
        tp_grau_academico                   AS codigo_grau_academico,
        tp_modalidade_ensino                AS codigo_modalidade_ensino,
        tp_nivel_academico                  AS codigo_nivel_academico,
        org_academica                       AS codigo_organizacao_academica,
        categoria                           AS codigo_categoria_administrativa,
        tp_rede                             AS codigo_rede,
        dimensao,
        in_gratuito,
        qt_vg_total,
        qt_mat                              AS qt_vg_mat,
        qt_ing                              AS qt_vg_ing,
        qt_conc                             AS qt_vg_conc,
        qt_sit_trancada,
        qt_sit_desvinculado                 AS qt_sit_desligado
    FROM superior_curso_censo
    WHERE ano_censo BETWEEN {ANO_MIN} AND {ANO_MAX}
    """,
    con,
)
con.close()

# Reduz drasticamente o uso de memoria (essencial numa fato de ~3,9M linhas): sem isso,
# o conector Python do Power BI precisa converter o DataFrame (que tem 2 colunas string
# misturadas com 15 numericas) para um array unico, forcando TUDO para dtype "object".
# codigo_cine_rotulo vira "category" (so 785 valores distintos repetidos ~4M vezes --
# ideal para category, que guarda so um indice inteiro por linha). As colunas inteiras
# recebem o menor dtype que comporta seus valores (downcast).
fato_curso_censo["codigo_cine_rotulo"] = fato_curso_censo["codigo_cine_rotulo"].astype("category")
for _col in [c for c in fato_curso_censo.columns if c != "codigo_cine_rotulo"]:
    fato_curso_censo[_col] = pd.to_numeric(fato_curso_censo[_col], downcast="integer")

# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
fato_ies_censo. Grao: uma linha por IES x ano_censo (~50 mil linhas), com a quantidade
de docentes em varios recortes (sexo, titulacao, regime de trabalho etc.).

Observacoes sobre os dados de origem: nao ha registros do Censo 2009; em 2005 cada IES
aparece em 2 linhas com valores fracionados (.5) que, somadas, preservam o total; e
`ies = 0` agrupa instituicoes nao identificadas.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"
ANO_MIN = 2004
ANO_MAX = 2024

con = sqlite3.connect(DB_PATH)
fato_ies_censo = pd.read_sql_query(
    f"""
    SELECT
        ano_censo                          AS codigo_ano,
        CAST(municipio AS INTEGER)         AS codigo_municipio,
        ies                                AS codigo_ies,
        mantenedora                        AS codigo_mantenedora,
        org_academica                      AS codigo_organizacao_academica,
        categoria                          AS codigo_categoria_administrativa,
        tp_rede                            AS codigo_rede,
        qt_doc_total,
        qt_doc_exe,
        qt_doc_ex_femi,
        qt_doc_ex_masc,
        qt_doc_ex_dout,
        qt_doc_ex_mest,
        qt_doc_ex_esp,
        qt_doc_ex_grad,
        qt_doc_ex_sem_grad,
        qt_doc_ex_int,
        qt_doc_ex_int_de,
        qt_doc_ex_parc,
        qt_doc_ex_hor,
        qt_doc_ex_com_deficiencia,
        qt_doc_ex_est
    FROM superior_ies_censo
    WHERE ano_censo BETWEEN {ANO_MIN} AND {ANO_MAX}
    """,
    con,
)
con.close()

# Menor dtype que comporta os valores (colunas com .5 de 2005 permanecem float).
for _col in fato_ies_censo.columns:
    fato_ies_censo[_col] = pd.to_numeric(fato_ies_censo[_col], downcast="integer")

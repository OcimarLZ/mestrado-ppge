# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_cine. Ver README.md na pasta powerbi/.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)

# cine_rotulo (tipo padronizado de curso) -> area_detalhada -> area_especifica ->
# area_geral, tudo achatado numa unica tabela (modelo em estrela).
# superior_cine_rotulo so tem (codigo, nome) -- SEM FK para area_detalhada. A ligacao e
# implicita: os digitos 2-4 do codigo do cine_rotulo (ex: "0113P01" -> "113") correspondem
# ao codigo de area_detalhada (113 = "Formacao de professores sem areas especificas").
# LIMITACAO CONHECIDA: esse parsing cobre ~91% dos rotulos (715 de 785). Quando a area
# geral tem 2 digitos (codigo 10 = "Servicos"), o codigo do cine_rotulo NAO tem o zero de
# preenchimento (ex: "1032S03" = area 1032, nao "032") -- inconsistencia real da fonte de
# dados do INEP, nao um bug de parsing. Nesses ~70 casos, nao ha area correspondente.
# Em vez de deixar NULL (pandas vira float64 por causa do NaN, e o Power BI rejeitou a
# conversao desses nulos para "double"/"Int64 anulavel" ao carregar o PBIP -- testado e
# nao funcionou), usamos COALESCE(..., -1) direto no SQL: -1 = "sem area mapeada", mantendo
# a coluna como inteiro comum (int64), sem nenhum nulo.
dim_cine = pd.read_sql_query(
    """
    SELECT
        cr.codigo                      AS codigo_cine_rotulo,
        cr.nome                        AS nome_cine_rotulo,
        COALESCE(ad.codigo, -1)        AS codigo_area_detalhada,
        COALESCE(ad.nome, 'Sem area mapeada') AS nome_area_detalhada,
        COALESCE(ae.codigo, -1)        AS codigo_area_especifica,
        COALESCE(ae.nome, 'Sem area mapeada') AS nome_area_especifica,
        COALESCE(ag.codigo, -1)        AS codigo_area_geral,
        COALESCE(ag.nome, 'Sem area mapeada') AS nome_area_geral
    FROM superior_cine_rotulo cr
    LEFT JOIN superior_area_detalhada ad ON ad.codigo = CAST(SUBSTR(cr.codigo, 2, 3) AS INTEGER)
    LEFT JOIN superior_area_especifica ae ON ae.codigo = ad.area_especifica
    LEFT JOIN superior_area ag ON ag.codigo = ae.area
    """,
    con,
)
con.close()

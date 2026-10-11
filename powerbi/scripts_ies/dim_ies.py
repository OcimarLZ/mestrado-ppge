# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_ies. Ver README.md na pasta powerbi/.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)

# Modelo em ESTRELA, nao em terceira forma normal (snowflake): cada dimensao se relaciona
# SO com a fato, nunca com outra dimensao. Por isso NAO trazemos aqui o municipio da IES
# como FK para dim_territorio (o territorio relevante para os paineis e o da OFERTA do
# curso, que a fato ja liga direto a dim_territorio via codigo_municipio) -- mantemos so
# atributos proprios da IES.
dim_ies = pd.read_sql_query(
    """
    SELECT
        codigo          AS codigo_ies,
        nome            AS nome_ies,
        sigla           AS sigla_ies
    FROM superior_ies
    """,
    con,
)
con.close()

# Codigo 0 = instituicoes nao identificadas no Censo (existe na fato, nao em superior_ies).
dim_ies = pd.concat(
    [dim_ies, pd.DataFrame({"codigo_ies": [0], "nome_ies": ["IES não identificada"], "sigla_ies": [None]})],
    ignore_index=True,
)
